"""
Эндпоинты синхронизации 'Диспетчер — Водитель'.
"""

from fastapi import APIRouter

router = APIRouter()


@router.get("/{driver_id}/route")
def get_driver_route(driver_id: int):
    """Текущий путевой лист водителя: последовательность адресов."""
    # TODO: выборка активного маршрута по vehicle/driver
    return {}


@router.post("/{driver_id}/complete-point")
def complete_point(driver_id: int, bin_id: int):
    """Водитель нажал 'Готово' после очистки контейнера."""
    # TODO: инициировать reset датчика (см. bins.reset_bin), отметить точку выполненной
    return {"status": "completed", "bin_id": bin_id}
