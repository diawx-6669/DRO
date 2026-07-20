"""
DRO — Dispatch Route Optimizer
Точка входа FastAPI-приложения.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import bins, routes, drivers, analytics
from app.core.config import settings

app = FastAPI(
    title="DRO — Dispatch Route Optimizer",
    description="API диспетчерской панели для оптимизации логистики вторичного сырья",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(bins.router, prefix="/api/bins", tags=["Контейнеры"])
app.include_router(routes.router, prefix="/api/routes", tags=["Маршруты"])
app.include_router(drivers.router, prefix="/api/drivers", tags=["Водители"])
app.include_router(analytics.router, prefix="/api/analytics", tags=["Аналитика"])


@app.get("/health")
def health_check():
    return {"status": "ok"}
