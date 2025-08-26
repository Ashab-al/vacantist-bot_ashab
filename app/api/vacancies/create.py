from fastapi import Depends, APIRouter, Body
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_async_session
from typing import Annotated
from schemas.api.vacancies.create.response import CreateVacancyResponse
from schemas.api.vacancies.create.request import CreateVacancyRequest
from services.api.vacancy.check_and_create_vacancy_then_send_to_users import check_and_create_vacancy_then_send_to_users

router = APIRouter()

@router.post(
    "/",
    summary="Создание новой вакансии.",
    description="Создает новую вакансию и отправляет эту вакансию пользователям.",
    response_model=CreateVacancyResponse
)
async def create_new_vacancy(
    session: Annotated[AsyncSession, Depends(get_async_session)],
    vacancy_data: Annotated[CreateVacancyRequest, Body()]
):
    new_vacancy = await check_and_create_vacancy_then_send_to_users(session, vacancy_data)
    
    return CreateVacancyResponse(**new_vacancy.dict())