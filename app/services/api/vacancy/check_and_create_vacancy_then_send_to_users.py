from sqlalchemy.ext.asyncio import AsyncSession
from models.vacancy import Vacancy
from models.category import Category
from sqlalchemy import (
    select,
)
from schemas.api.vacancies.create.request import CreateVacancyRequest
from services.api.vacancy.black_list_check import black_list_check
from services.api.vacancy.create_vacancy import create_vacancy
from repositories.categories.get_category_by_name import get_category_by_name

async def check_and_create_vacancy_then_send_to_users(
    db: AsyncSession,
    vacancy_data: CreateVacancyRequest
) -> Vacancy:
    """
    Проверить и создать вакансию, а затем разослать её пользователям.
    
    Args:
        db (AsyncSession): Активная сессия БД.
        vacancy_data (CreateVacancyRequest): 
            Pydantic-схема с данными для создания вакансии:
              - title (str): Заголовок вакансии
              - category_title (str): Название категории
              - description (str): Описание вакансии
              - contact_information (str): Контактные данные для связи
              - source (str): Источник вакансии
              - platform_id (int): ID отправителя
    
    Returns:
        Vacancy: Созданная вакансия.
    """
    blacklist = await black_list_check(
        db, 
        vacancy_data.platform_id, 
        vacancy_data.contact_information
    )
    if blacklist:
        raise ValueError("Вакансия в черном списке")
    
    category = await get_category_by_name(
        db, 
        vacancy_data.category_title
    )

    if not category:
        raise ValueError("Такой категории не существует")
    
    # TODO

