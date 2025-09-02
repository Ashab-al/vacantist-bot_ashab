from sqlalchemy.ext.asyncio import AsyncSession
from models.vacancy import Vacancy
from models.category import Category
from sqlalchemy import (
    select,
)
from schemas.api.vacancies.create.request import CreateVacancyRequest


async def create_vacancy(
    db: AsyncSession,
    vacancy_data: CreateVacancyRequest,
    category: Category
) -> Vacancy:
    vacancy: Vacancy = Vacancy(
        title=vacancy_data.title,
        description=vacancy_data.description,
        contact_information=vacancy_data.contact_information,
        source=vacancy_data.source,
        platform_id=vacancy_data.platform_id,
        category=category 
    )

    db.add(vacancy)
    await db.commit()
    await db.refresh(vacancy)

    return vacancy