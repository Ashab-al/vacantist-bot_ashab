from math import ceil

from enums.vacancies_for_the_week_enum import VacanciesForTheWeekStatusEnum
from models.category import Category
from models.user import User
from models.vacancy import Vacancy
from query_objects.vacancies.vacancies_for_the_week import VacancyForTheWeekQuery
from services.tg.category.find_subscribe import find_subscribe
from sqlalchemy.ext.asyncio import AsyncSession


async def fetch_vacancies_for_the_week(
    db: AsyncSession, user: User, page: int, page_size: int
) -> dict:
    """
    Возвращает список вакансий за неделю с поддержкой пагинации

    Args:
        db (AsyncSession): Асинхронная сессия SQLAlchemy для работы с базой данных.
        user (User): Пользователь, для которого выполняется выборка.
        page (int): Номер страницы (начиная с 1).
        page_size (int): Количество элементов на странице.

    Returns:
        dict: Словарь с результатом выборки.
            - status (VacanciesForTheWeekStatusEnum): Статус выполнения
            - items (list[Vacancy]): Список вакансий для текущей страницы (если есть)
            - meta (dict): Метаданные пагинации с ключами:
                - count (int): Общее количество вакансий
                - page (int): Текущая страница
                - max_pages (int): Общее количество страниц

    Notes:
        - Если у пользователя нет подписки на категории, возвращается:
            {"status": SUBSCRIBED_CATEGORIES_EMPTY}
        - Если вакансий не найдено, возвращается:
            {"status": VACANCY_LIST_EMPTY}
    """
    subscribed_categories: list[Category] | list = await find_subscribe(db, user)

    if not subscribed_categories:
        return {"status": VacanciesForTheWeekStatusEnum.SUBSCRIBED_CATEGORIES_EMPTY}
    vacancy_for_the_week_repo = VacancyForTheWeekQuery(db, user, page, page_size)
    vacancies: list[Vacancy] | list = (
        await vacancy_for_the_week_repo.build_vacancies_for_the_week(
            subscribed_categories
        )
    )
    if not vacancies:
        return {"status": VacanciesForTheWeekStatusEnum.VACANCY_LIST_EMPTY}

    total: int = await vacancy_for_the_week_repo.total_count()
    max_pages: int = ceil(total / page_size)
    return {
        "status": VacanciesForTheWeekStatusEnum.OK,
        "items": vacancies,
        "meta": {"count": total, "page": page, "max_pages": max_pages},
    }
