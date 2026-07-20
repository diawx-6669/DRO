"""
Эндпоинты для контейнеров и приема телеметрии от датчиков ESP32.
"""

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


class SensorTelemetry(BaseModel):
    bin_id: int
    fill_percent: float
    battery_level: float


@router.get("/")
def list_bins():
    """Возвращает список всех контейнеров с текущим статусом заполнения."""
    # TODO: выборка из БД (PostGIS) со статусом green/yellow/red по fill_percent
    return []


@router.get("/{bin_id}")
def get_bin(bin_id: int):
    """Детальная карточка контейнера: адрес, % заполнения, заряд батареи, история."""
    # TODO: выборка бака + история за неделю из sensor_readings
    return {}


@router.post("/telemetry")
def receive_telemetry(payload: SensorTelemetry):
    """Прием данных от датчика ESP32 (HTTP POST) и обновление статуса бака."""
    # TODO: сохранить в sensor_readings, обновить bins.fill_percent
    return {"status": "received"}


@router.post("/{bin_id}/reset")
def reset_bin(bin_id: int):
    """Принудительный опрос датчика после того, как водитель нажал 'Готово'."""
    # TODO: отправить MQTT-команду на датчик, обнулить fill_percent
    return {"status": "reset_requested"}
