from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings
from app.db.models import Base

# Railway часто отдаёт DATABASE_URL со схемой postgres:// — SQLAlchemy 2.x
# требует postgresql://, поэтому нормализуем на лету.
db_url = settings.DATABASE_URL
if db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql://", 1)

engine = create_engine(db_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Создаёт все таблицы, если их ещё нет. Вызывается при старте приложения."""
    Base.metadata.create_all(bind=engine)
