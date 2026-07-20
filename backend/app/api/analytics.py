"""
Эндпоинты модуля бизнес-аналитики (BI).
"""

from fastapi import APIRouter

router = APIRouter()


@router.get("/fuel-savings")
def fuel_savings():
    """Сравнение реального пробега (оптимизированного) с гипотетическим объездом всех точек."""
    # TODO: расчет экономии ГСМ в литрах и тенге
    return {}


@router.get("/collection-stats")
def collection_stats():
    """Статистика объема собранного сырья по дням/неделям/месяцам."""
    return {}


@router.get("/fast-filling-bins")
def fast_filling_bins():
    """Рейтинг контейнеров/дворов с аномально высокой скоростью заполнения."""
    return {}
