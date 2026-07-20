from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # База данных
    DATABASE_URL: str = "postgresql://dro_user:dro_pass@localhost:5432/dro_db"

    # MQTT-брокер для приема данных с датчиков ESP32
    MQTT_BROKER_HOST: str = "localhost"
    MQTT_BROKER_PORT: int = 1883
    MQTT_TOPIC_TELEMETRY: str = "dro/bins/+/telemetry"

    # Бизнес-логика
    FILL_THRESHOLD_PERCENT: int = 80  # порог включения бака в маршрут

    # CORS
    CORS_ORIGINS: list[str] = ["http://localhost:5173", "http://localhost:3000"]

    class Config:
        env_file = ".env"


settings = Settings()
