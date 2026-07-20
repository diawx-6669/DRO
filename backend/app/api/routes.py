"""
Эндпоинты построения и управления маршрутами (VRP).
"""

from fastapi import APIRouter

from app.services.route_optimizer import build_optimal_route

router = APIRouter()


@router.post("/generate")
def generate_route():
    """
    Строит оптимальный маршрут по всем контейнерам с fill_percent >= порога (80%).
    Использует OR-Tools для решения задачи VRP.
    """
    route = build_optimal_route()
    return route


@router.post("/{route_id}/assign")
def assign_route(route_id: int, vehicle_id: int):
    """Назначает маршрут (или его сегмент) конкретному водителю/автомобилю."""
    # TODO: обновить Route.vehicle_id, отправить уведомление в Telegram-бот
    return {"status": "assigned", "route_id": route_id, "vehicle_id": vehicle_id}


@router.get("/{route_id}")
def get_route(route_id: int):
    """Возвращает детали маршрута: последовательность точек, дистанцию, статус."""
    # TODO: выборка из БД
    return {}
