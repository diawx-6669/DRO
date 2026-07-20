"""
Ядро алгоритмического модуля: построение оптимального маршрута (VRP)
через Google OR-Tools для всех контейнеров, заполненных >= FILL_THRESHOLD_PERCENT.
"""

from app.core.config import settings


def get_filtered_bins():
    """Отбирает контейнеры с fill_percent >= порога (80%)."""
    # TODO: SELECT * FROM bins WHERE fill_percent >= settings.FILL_THRESHOLD_PERCENT
    return []


def build_distance_matrix(points: list[tuple[float, float]]) -> list[list[float]]:
    """Строит матрицу расстояний между точками (депо + отобранные баки + пункт выгрузки)."""
    # TODO: расчет через геокоординаты (haversine) или внешний Routing API
    return []


def build_optimal_route():
    """
    Решает задачу VRP через OR-Tools:
    депо -> цепочка заполненных контейнеров -> пункт выгрузки/прессования,
    минимизируя суммарный километраж.
    """
    bins = get_filtered_bins()
    if not bins:
        return {"points": [], "total_distance_km": 0}

    # TODO: matrix = build_distance_matrix(...)
    # TODO: routing = pywrapcp.RoutingModel(...) — стандартная схема OR-Tools VRP

    return {
        "points": bins,
        "total_distance_km": None,  # заполняется после расчета OR-Tools
    }
