from models.user import User
from models.vacancy import Vacancy
from models.category import Category
from sqlalchemy.ext.asyncio import AsyncSession
from enums.vacancies_for_the_week_enum import VacanciesForTheWeekStatusEnum
from repositories.vacancies.vacancies_for_the_week import VacancyForTheWeekRepository
from services.tg.category.find_subscribe import find_subscribe
from math import ceil


async def fetch_vacancies_for_the_week(
    db: AsyncSession,
    user: User,
    page: int,
    page_size: int
) -> dict:
    """
    Вернуть вакансии за неделю для пагинации.

    Args:
        db (AsyncSession): Асинхронная сессия SQLAlchemy для работы с базой данных.
        user (User): Объект пользователя.
        page (int): Номер страницы.
        page_size (int): Размер страницы.
    
    Returns:
        dict: Словарь с ключами `status`, `items`, `meta`.
    
    Notes:
        - Если у пользователя нет подписки на какую-либо категорию, 
        то возвращается словарь только с одним ключом `status`, 
        у которого значение `SUBSCRIBED_CATEGORIES_EMPTY`
        - Если не найдено вакансий, то возвращается словарь только с одним ключом `status`,
        у которого значение `VACANCY_LIST_EMPTY`
    """
    subscribed_categories: list[Category] | list = await find_subscribe(db, user)

    if not subscribed_categories:
        return {
            "status": VacanciesForTheWeekStatusEnum.SUBSCRIBED_CATEGORIES_EMPTY
        }
    vacancy_for_the_week_repo = VacancyForTheWeekRepository(
        db,
        subscribed_categories,
        user,
        page,
        page_size
    )
    vacancies: list[Vacancy] | list = await vacancy_for_the_week_repo.build_vacancies_for_the_week()
    if not vacancies:
        return {
            "status": VacanciesForTheWeekStatusEnum.VACANCY_LIST_EMPTY    
        }

    total: int = await vacancy_for_the_week_repo.total_count()
    max_pages: int = ceil(total / page_size)
    return {
        "status": VacanciesForTheWeekStatusEnum.OK,
        "items": vacancies,
        "meta": {
            "count": total,
            "page": page,
            "max_pages": max_pages
        }
    }