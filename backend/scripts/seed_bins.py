"""
Наполняет БД тестовыми контейнерами вокруг Астаны — чтобы сразу
увидеть маркеры на карте (зелёные / жёлтые / красные).

Запуск:
    cd backend
    python -m scripts.seed_bins
"""

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from app.db.models import Bin
from app.db.session import SessionLocal, init_db

TEST_BINS = [
    {"address": "ул. Кенесары, 42", "lat": 51.1801, "lng": 71.4460, "fill_percent": 92, "battery_level": 78},
    {"address": "пр. Республики, 15", "lat": 51.1694, "lng": 71.4491, "fill_percent": 15, "battery_level": 95},
    {"address": "ул. Достык, 8", "lat": 51.1284, "lng": 71.4306, "fill_percent": 65, "battery_level": 60},
    {"address": "мкр. Тельман, 3", "lat": 51.1105, "lng": 71.4102, "fill_percent": 88, "battery_level": 40},
    {"address": "ул. Сарыарка, 25", "lat": 51.1550, "lng": 71.4050, "fill_percent": 30, "battery_level": 88},
    {"address": "пр. Туран, 55", "lat": 51.0967, "lng": 71.4186, "fill_percent": 55, "battery_level": 72},
    {"address": "ул. Кабанбай батыра, 11", "lat": 51.1289, "lng": 71.4699, "fill_percent": 96, "battery_level": 25},
    {"address": "мкр. Железнодорожный, 7", "lat": 51.1650, "lng": 71.4950, "fill_percent": 8, "battery_level": 99},
]


def seed():
    init_db()
    db = SessionLocal()
    try:
        existing = db.query(Bin).count()
        if existing > 0:
            print(f"В БД уже есть {existing} контейнер(ов). Пропускаю сидинг.")
            return

        for data in TEST_BINS:
            db.add(Bin(**data))
        db.commit()
        print(f"Добавлено {len(TEST_BINS)} тестовых контейнеров.")
    finally:
        db.close()


if __name__ == "__main__":
    seed()
