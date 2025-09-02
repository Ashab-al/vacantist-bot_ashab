from models.vacancy import Vacancy
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload


async def get_all_vacancies(
    db: AsyncSession
) -> list[Vacancy]:
    vacancies = (
        await db.execute(select(Vacancy).options(joinedload(Vacancy.category)))
    ).scalars().all()
    
    return vacancies