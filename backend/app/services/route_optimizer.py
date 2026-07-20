"""
Ядро алгоритмического модуля: построение оптимального маршрута (VRP)
через Google OR-Tools для всех контейнеров, заполненных >= FILL_THRESHOLD_PERCENT.

Маршрут строится от депо (условная точка автопарка) через все "красные"
контейнеры до пункта выгрузки/прессования, минимизируя суммарный километраж.
"""

import math

from ortools.constraint_solver import pywrapcp, routing_enums_pb2
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.models import Bin

# Условные координаты депо и пункта выгрузки (задать реальные при внедрении)
DEPOT_COORDS = (51.1605, 71.4704)  # автопарк
UNLOADING_COORDS = (51.1801, 71.4460)  # пункт выгрузки/прессования


def haversine_km(coord1, coord2):
    """Расстояние между двумя точками (lat, lng) по формуле гаверсинуса, в км."""
    lat1, lon1 = coord1
    lat2, lon2 = coord2
    r = 6371.0
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    return 2 * r * math.asin(math.sqrt(a))


def get_filtered_bins(db: Session):
    """Отбирает контейнеры с fill_percent >= порога (по умолчанию 80%)."""
    return (
        db.query(Bin)
        .filter(Bin.fill_percent >= settings.FILL_THRESHOLD_PERCENT)
        .all()
    )


def build_distance_matrix(points: list[tuple[float, float]]) -> list[list[int]]:
    """
    Строит матрицу расстояний между точками (в метрах, целые числа —
    OR-Tools работает с int-стоимостями).
    """
    size = len(points)
    matrix = [[0] * size for _ in range(size)]
    for i in range(size):
        for j in range(size):
            if i != j:
                matrix[i][j] = int(haversine_km(points[i], points[j]) * 1000)
    return matrix


def solve_vrp(points: list[tuple[float, float]]) -> tuple[list[int], float]:
    """
    Решает задачу VRP для одного транспортного средства: депо (индекс 0) ->
    все точки -> пункт выгрузки (последний индекс).
    Возвращает (порядок индексов точек, суммарная дистанция в км).
    """
    matrix = build_distance_matrix(points)
    n = len(points)

    manager = pywrapcp.RoutingIndexManager(n, 1, [0], [n - 1])
    routing = pywrapcp.RoutingModel(manager)

    def distance_callback(from_index, to_index):
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return matrix[from_node][to_node]

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
    )

    solution = routing.SolveWithParameters(search_parameters)
    if not solution:
        return list(range(n)), 0.0

    order = []
    index = routing.Start(0)
    total_distance_m = 0
    while not routing.IsEnd(index):
        order.append(manager.IndexToNode(index))
        prev_index = index
        index = solution.Value(routing.NextVar(index))
        total_distance_m += routing.GetArcCostForVehicle(prev_index, index, 0)
    order.append(manager.IndexToNode(index))

    return order, total_distance_m / 1000.0


def build_optimal_route(db: Session):
    """
    Полный пайплайн: депо -> отобранные заполненные контейнеры -> пункт выгрузки,
    с минимизацией суммарного километража.
    """
    bins = get_filtered_bins(db)
    if not bins:
        return {"points": [], "total_distance_km": 0, "message": "Нет контейнеров, заполненных выше порога"}

    coords = [DEPOT_COORDS] + [(b.lat, b.lng) for b in bins] + [UNLOADING_COORDS]
    order, total_distance_km = solve_vrp(coords)

    labels = ["Депо"] + [f"{b.address} ({b.fill_percent:.0f}%)" for b in bins] + ["Пункт выгрузки"]
    ids = [None] + [b.id for b in bins] + [None]

    ordered_points = [
        {"label": labels[i], "bin_id": ids[i], "lat": coords[i][0], "lng": coords[i][1]}
        for i in order
    ]

    return {
        "points": ordered_points,
        "total_distance_km": round(total_distance_km, 2),
        "bins_count": len(bins),
    }
