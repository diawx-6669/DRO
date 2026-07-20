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
def seed_test_bins(db: Session = Depends(get_db)):
    """
    Разово наполняет БД тестовыми контейнерами вокруг Астаны для проверки карты.
    Безопасно вызывать повторно — если баки уже есть, ничего не добавляет.
    """
    if db.query(Bin).count() > 0:
        return {"status": "skipped", "reason": "bins already exist"}

    test_bins = [
        {"address": "ул. Кенесары, 42", "lat": 51.1801, "lng": 71.4460, "fill_percent": 92, "battery_level": 78},
        {"address": "пр. Республики, 15", "lat": 51.1694, "lng": 71.4491, "fill_percent": 15, "battery_level": 95},
        {"address": "ул. Достык, 8", "lat": 51.1284, "lng": 71.4306, "fill_percent": 65, "battery_level": 60},
        {"address": "мкр. Тельман, 3", "lat": 51.1105, "lng": 71.4102, "fill_percent": 88, "battery_level": 40},
        {"address": "ул. Сарыарка, 25", "lat": 51.1550, "lng": 71.4050, "fill_percent": 30, "battery_level": 88},
        {"address": "пр. Туран, 55", "lat": 51.0967, "lng": 71.4186, "fill_percent": 55, "battery_level": 72},
        {"address": "ул. Кабанбай батыра, 11", "lat": 51.1289, "lng": 71.4699, "fill_percent": 96, "battery_level": 25},
        {"address": "мкр. Железнодорожный, 7", "lat": 51.1650, "lng": 71.4950, "fill_percent": 8, "battery_level": 99},
    ]
    for data in test_bins:
        db.add(Bin(**data))
    db.commit()

    return {"status": "seeded", "count": len(test_bins)}
