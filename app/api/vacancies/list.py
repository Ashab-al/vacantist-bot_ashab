from fastapi import Depends, APIRouter, Body, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_async_session
from typing import Annotated
from repositories.vacancies.get_all_vacancies import get_all_vacancies
from models.vacancy import Vacancy
from schemas.api.vacancies.vacancy import VacancySchema
from services.api.vacancy.vacancies_list import vacancies_list


router = APIRouter()

@router.get(
    "/",
    summary="Получить все вакансии.",
    description=(
        "Возвращает список всех вакансий из базы данных.\n\n"
        "Каждая вакансия содержит:\n"
        "- `id` — уникальный идентификатор вакансии\n"
        "- `title` — заголовок вакансии\n"
        "- `description` — описание\n"
        "- `contact_information` — контакты для связи\n"
        "- `source` — источник (например, Telegram)\n"
        "- `platform_id` — идентификатор отправителя\n"
        "- `category_title` — название категории вакансии\n\n"
    ),
    response_model=list[VacancySchema],
    response_description="Список вакансий в формате JSON"
)
async def list_vacancies(
    session: Annotated[AsyncSession, Depends(get_async_session)]
):
    """
    Вернуть список вакансий
    """
    vacancies_to_schema: list[VacancySchema] = await vacancies_list(session)
    return vacancies_to_schema