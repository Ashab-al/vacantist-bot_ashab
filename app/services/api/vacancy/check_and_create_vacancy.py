from models.category import Category
from models.vacancy import Vacancy
from repositories.categories.get_category_by_name import get_category_by_name
from schemas.api.vacancies.create.request import CreateVacancyRequest
from services.api.vacancy.black_list_check import black_list_check
from services.api.vacancy.create_vacancy import create_vacancy
from sqlalchemy.ext.asyncio import AsyncSession


async def check_and_create_vacancy(
    db: AsyncSession, vacancy_data: CreateVacancyRequest
) -> Vacancy:
    """
    Проверить и создать вакансию.

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

    Raises:
        ValueError: Вакансия в черном списке
        ValueError: Такой категории не существует
        Exception: Непредвиденная ошибка. Метод black_list_check
    """
    try:
        await black_list_check(
            db, vacancy_data.platform_id, vacancy_data.contact_information
        )
    except ValueError:
        raise
    except Exception as e:
        e.add_note("Непредвиденная ошибка. Метод black_list_check")
        raise

    category: Category = await get_category_by_name(db, vacancy_data.category_title)

    if not category:
        raise ValueError("Такой категории не существует")

    vacancy: Vacancy = await create_vacancy(db, vacancy_data, category)

    return vacancy
