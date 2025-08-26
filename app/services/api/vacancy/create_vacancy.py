from sqlalchemy.ext.asyncio import AsyncSession
from models.vacancy import Vacancy
from sqlalchemy import (
    select,
)
from schemas.api.vacancies.create.request import CreateVacancyRequest


async def create_vacancy(
    db: AsyncSession,
    vacancy_data: CreateVacancyRequest
) -> Vacancy:
    ...