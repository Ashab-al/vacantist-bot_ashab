from models.vacancy import Vacancy
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload


async def get_all_vacancies(
    db: AsyncSession
) -> list[Vacancy]:
    """
    Получить список всех вакансий с предзагруженной категорией.

    Args:
        db (AsyncSession): Асинхронная сессия SQLAlchemy для работы с базой данных.

    Returns:
        list[Vacancy]: Список всех вакансий с загруженной категорией.
    """
    return (
        await db.execute(select(Vacancy).options(joinedload(Vacancy.category)))
    ).scalars().all()