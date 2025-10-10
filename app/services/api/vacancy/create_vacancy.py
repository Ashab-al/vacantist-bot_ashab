from sqlalchemy.ext.asyncio import AsyncSession
from models.vacancy import Vacancy
from models.category import Category
from schemas.api.vacancies.create.request import CreateVacancyRequest


async def create_vacancy(
    db: AsyncSession, vacancy_data: CreateVacancyRequest, category: Category
) -> Vacancy:
    """
    Создать вакансию

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
        category (Category): Объект категории к которому относится вакансия

    Returns:
        Vacancy: Созданная вакансия
    """
    vacancy: Vacancy = Vacancy(
        title=vacancy_data.title,
        description=vacancy_data.description,
        contact_information=vacancy_data.contact_information,
        source=vacancy_data.source,
        platform_id=vacancy_data.platform_id,
        category=category,
    )

    db.add(vacancy)
    await db.commit()
    await db.refresh(vacancy)

    return vacancy
