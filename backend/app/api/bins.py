"""
Эндпоинты для контейнеров и приема телеметрии от датчиков ESP32.
"""

from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.db.models import Bin, SensorReading
from app.db.session import get_db

router = APIRouter()


class SensorTelemetry(BaseModel):
    bin_id: int
    fill_percent: float
    battery_level: float


@router.get("/")
def list_bins(db: Session = Depends(get_db)):
    """Возвращает список всех контейнеров с текущим статусом заполнения."""
    bins = db.query(Bin).all()
    return [
        {
            "id": b.id,
            "address": b.address,
            "lat": b.lat,
            "lng": b.lng,
            "fill_percent": b.fill_percent,
            "battery_level": b.battery_level,
            "last_seen_at": b.last_seen_at,
        }
        for b in bins
    ]


@router.get("/{bin_id}")
def get_bin(bin_id: int, db: Session = Depends(get_db)):
    """Детальная карточка контейнера: адрес, % заполнения, заряд батареи, история за неделю."""
    b = db.query(Bin).filter(Bin.id == bin_id).first()
    if not b:
        raise HTTPException(status_code=404, detail="Контейнер не найден")

    week_ago = datetime.utcnow() - timedelta(days=7)
    history = (
        db.query(SensorReading)
        .filter(SensorReading.bin_id == bin_id, SensorReading.recorded_at >= week_ago)
        .order_by(SensorReading.recorded_at.asc())
        .all()
    )

    return {
        "id": b.id,
        "address": b.address,
        "lat": b.lat,
        "lng": b.lng,
        "fill_percent": b.fill_percent,
        "battery_level": b.battery_level,
        "last_seen_at": b.last_seen_at,
        "history": [
            {"recorded_at": h.recorded_at, "fill_percent": h.fill_percent}
            for h in history
        ],
    }


@router.post("/telemetry")
def receive_telemetry(payload: SensorTelemetry, db: Session = Depends(get_db)):
    """Прием данных от датчика ESP32 (HTTP POST) и обновление статуса бака."""
    b = db.query(Bin).filter(Bin.id == payload.bin_id).first()
    if not b:
        raise HTTPException(status_code=404, detail="Контейнер не найден")

    b.fill_percent = payload.fill_percent
    b.battery_level = payload.battery_level
    b.last_seen_at = datetime.utcnow()

    reading = SensorReading(
        bin_id=payload.bin_id,
        fill_percent=payload.fill_percent,
        battery_level=payload.battery_level,
    )
    db.add(reading)
    db.commit()

    return {"status": "received"}


@router.post("/{bin_id}/reset")
def reset_bin(bin_id: int, db: Session = Depends(get_db)):
    """Вызывается водителем после очистки контейнера — обнуляет заполнение."""
    b = db.query(Bin).filter(Bin.id == bin_id).first()
    if not b:
        raise HTTPException(status_code=404, detail="Контейнер не найден")

    b.fill_percent = 0.0
    b.last_seen_at = datetime.utcnow()
    db.commit()

    return {"status": "reset_done", "bin_id": bin_id}


@router.post("/seed")
def seed_single_demo_bin(db: Session = Depends(get_db)):
    """
    Очищает базу и оставляет ровно один контейнер — тот самый макет
    с настоящим датчиком, который будет обновляться через /telemetry
    (в том числе из окна «Проверка датчика» на сайте).
    Безопасно вызывать повторно — просто пересоздаёт этот единственный бак.
    """
    db.query(SensorReading).delete()
    db.query(Bin).delete()
    db.commit()

    demo_bin = Bin(
        address="Демо-стенд — реальный датчик",
        lat=51.1801,
        lng=71.4460,
        fill_percent=0.0,
        battery_level=100.0,
    )
    db.add(demo_bin)
    db.commit()
    db.refresh(demo_bin)

    return {"status": "seeded", "bin_id": demo_bin.id, "count": 1}
