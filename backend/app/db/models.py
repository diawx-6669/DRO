"""
Модели данных для PostgreSQL.

Примечание: изначально координаты планировались через PostGIS (Geometry),
но для MVP на Railway используем обычные float lat/lng — это не требует
включения расширения PostGIS на управляемой БД и упрощает деплой.
"""

from datetime import datetime

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Bin(Base):
    """Контейнер для сбора вторичного сырья."""

    __tablename__ = "bins"

    id = Column(Integer, primary_key=True, index=True)
    address = Column(String, nullable=False)
    lat = Column(Float, nullable=False)
    lng = Column(Float, nullable=False)
    fill_percent = Column(Float, default=0.0)
    battery_level = Column(Float, default=100.0)
    last_seen_at = Column(DateTime, default=datetime.utcnow)

    readings = relationship("SensorReading", back_populates="bin")


class SensorReading(Base):
    """Историческая запись показаний датчика (для TimescaleDB)."""

    __tablename__ = "sensor_readings"

    id = Column(Integer, primary_key=True, index=True)
    bin_id = Column(Integer, ForeignKey("bins.id"))
    fill_percent = Column(Float, nullable=False)
    battery_level = Column(Float, nullable=False)
    recorded_at = Column(DateTime, default=datetime.utcnow, index=True)

    bin = relationship("Bin", back_populates="readings")


class Vehicle(Base):
    """Транспортное средство автопарка."""

    __tablename__ = "vehicles"

    id = Column(Integer, primary_key=True, index=True)
    plate_number = Column(String, unique=True, nullable=False)
    driver_name = Column(String, nullable=False)
    telegram_chat_id = Column(String, nullable=True)


class Route(Base):
    """Сгенерированный маршрут на день."""

    __tablename__ = "routes"

    id = Column(Integer, primary_key=True, index=True)
    vehicle_id = Column(Integer, ForeignKey("vehicles.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    total_distance_km = Column(Float, nullable=True)
    status = Column(String, default="planned")  # planned | in_progress | completed
