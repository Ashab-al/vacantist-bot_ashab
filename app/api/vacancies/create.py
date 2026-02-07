from typing import Annotated

from database import get_async_session
from exceptions.vacancy.blacklisted_vacancy import BlacklistedVacancyError
from fastapi import APIRouter, BackgroundTasks, Body, Depends, HTTPException
from schemas.api.vacancies.create.request import CreateVacancyRequest
from schemas.api.vacancies.create.response import CreateVacancyResponse
from services.api.vacancy.check_and_create_vacancy import check_and_create_vacancy
from services.tg.vacancy.sender_vacancy import sender_vacancy
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()


@router.post(
    "/",
    summary="Создание новой вакансии.",
    description="Создает новую вакансию и отправляет эту вакансию пользователям.",
    response_model=CreateVacancyResponse,
)
async def create_new_vacancy(
    session: Annotated[AsyncSession, Depends(get_async_session)],
    vacancy_data: Annotated[CreateVacancyRequest, Body()],
    background_tasks: BackgroundTasks,
):
    """
    Создать новую вакансию и отправить её пользователям.

    Эндпоинт проверяет данные вакансии, сохраняет их в базе данных
    и добавляет вакансию в очередь рассылки пользователям.

    Args:
        session (AsyncSession): Асинхронная сессия SQLAlchemy для взаимодействия с базой данных.
        vacancy_data (CreateVacancyRequest): Данные новой вакансии
            (название, описание, контакты, категория и др.).

    Raises:
        HTTPException: Ошибка 400, если создание вакансии не удалось.

    Returns:
        CreateVacancyResponse: Данные созданной вакансии
            (id, название, описание, контакты, источник, платформа).
    """
    try:
        new_vacancy = await check_and_create_vacancy(session, vacancy_data)
    except BlacklistedVacancyError as e:
        raise HTTPException(400, str(e)) from e
    # Добавляем задачу отправки вакансии в фоновый режим
    background_tasks.add_task(sender_vacancy, new_vacancy.id)

    return CreateVacancyResponse(
        id=new_vacancy.id,
        title=new_vacancy.title,
        category_title=vacancy_data.category_title,
        description=new_vacancy.description,
        contact_information=new_vacancy.contact_information,
        source=new_vacancy.source,
        platform_id=new_vacancy.platform_id,
    )
