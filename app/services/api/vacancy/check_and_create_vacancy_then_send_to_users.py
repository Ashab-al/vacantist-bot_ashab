from sqlalchemy.ext.asyncio import AsyncSession
from models.vacancy import Vacancy
from sqlalchemy import (
    select,
)
from schemas.api.vacancies.create.request import CreateVacancyRequest


async def check_and_create_vacancy_then_send_to_users(
    db: AsyncSession,
    vacancy_data: CreateVacancyRequest
) -> Vacancy:
    ...