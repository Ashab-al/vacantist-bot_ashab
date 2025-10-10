from models.vacancy import Vacancy
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import joinedload


async def find_vacancy_by_id(db: AsyncSession, vacancy_id: int) -> Vacancy | None:
    """
    Получить вакансию по её ID с предзагруженной категорией.

    Args:
        db (AsyncSession): Асинхронная сессия SQLAlchemy для работы с базой данных.
        vacancy_id (int): ID вакансии.

    Returns:
        Vacancy | None: Вакансия с предзагруженной категорией или None, если не найдена.
    """
    return (
        (
            await db.execute(
                select(Vacancy)
                .options(joinedload(Vacancy.category))
                .where(Vacancy.id == vacancy_id)
            )
        )
        .unique()
        .scalars()
        .first()
    )
