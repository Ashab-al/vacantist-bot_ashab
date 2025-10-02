from models.vacancy import Vacancy
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import joinedload

async def find_vacancy_by_id(
    db: AsyncSession,
    vacancy_id: int
) -> Vacancy | None:
    """Вернуть вакансию по id"""
    return (
        await db.execute(
            select(Vacancy).options(joinedload(Vacancy.category)).where(Vacancy.id==vacancy_id)
        )
    ).unique().scalars().first()