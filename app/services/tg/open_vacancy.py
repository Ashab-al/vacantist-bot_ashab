from enums.check_vacancy_enum import CheckVacancyEnum
from lib.tg.constants import SOURCE
from models.user import User
from models.vacancy import Vacancy
from repositories.blacklist.black_list_check_by_platform_id_and_contact_information import \
    black_list_check_by_platform_id_or_contact_information
from repositories.vacancies.find_vacancy_by_id import find_vacancy_by_id
from services.tg.spam_vacancy import COMPLAINT_COUNTER
from sqlalchemy.ext.asyncio import AsyncSession

REDUCE_BALANCE = 1
ZERO_BALANCE = 0
POINTS_EDGE = 5


async def open_vacancy(db: AsyncSession, user: User, vacancy_id: int) -> dict:
    """
    Открывает вакансию для пользователя с проверкой баланса и черного списка.

    Args:
        db (AsyncSession): Асинхронная сессия SQLAlchemy.
        user (User): Объект пользователя.
        vacancy_id (int): ID вакансии для открытия.

    Returns:
        dict: Результат операции с полями:
            - status: статус действия (`OPEN_VACANCY` или `WARNING`),
            - vacancy: объект вакансии (если применимо),
            - path_view: путь для templates,
            - low_points: True, если очки пользователя меньше или равны POINTS_EDGE.

    Raises:
        ValueError: Если вакансия с указанным ID не найдена.
    """
    vacancy: Vacancy = await find_vacancy_by_id(db, vacancy_id)
    if not vacancy:
        raise ValueError(f"{vacancy_id} - такой вакансии нет в базе данных")

    return await _check_vacancy(db, user, vacancy)


async def _check_vacancy(db: AsyncSession, user: User, vacancy: Vacancy) -> dict:
    """
    Проверяет возможность открытия вакансии пользователем и списывает баллы.

    Args:
        db (AsyncSession): Асинхронная сессия SQLAlchemy.
        user (User): Объект пользователя.
        vacancy (Vacancy): Объект вакансии.

    Returns:
        dict: Результат проверки с полями:
            - status: статус действия (`OPEN_VACANCY` или `WARNING`),
            - vacancy: объект вакансии (если применимо),
            - path_view: путь для templates,
            - low_points: True, если очки пользователя меньше или равны POINTS_EDGE.
    """
    if user.bonus + user.point <= ZERO_BALANCE:
        return {
            "status": CheckVacancyEnum.WARNING,
            "path_view": "callback_query/out_of_points",
        }

    contact_information: str = (
        vacancy.platform_id if vacancy.source == SOURCE else vacancy.contact_information
    )

    if await _check_blacklist(db, contact_information):
        return {
            "status": CheckVacancyEnum.WARNING,
            "vacancy": vacancy,
            "path_view": "callback_query/add_to_blacklist",
        }

    if user.bonus > ZERO_BALANCE:
        user.bonus = user.bonus - REDUCE_BALANCE
    else:
        user.point = user.point - REDUCE_BALANCE

    await db.commit()
    await db.refresh(user)
    await db.refresh(vacancy)

    return {
        "status": CheckVacancyEnum.OPEN_VACANCY,
        "vacancy": vacancy,
        "path_view": "callback_query/open_vacancy",
        "low_points": user.point <= POINTS_EDGE,
    }


async def _check_blacklist(db: AsyncSession, contact_information: str) -> bool:
    """
    Проверяет, находится ли контактная информация в черном списке.

    Args:
        db (AsyncSession): Асинхронная сессия SQLAlchemy.
        contact_information (str): Контактная информация вакансии (platform_id или контакт).

    Returns:
        bool: True, если контактная информация есть в черном списке и количество жалоб
              превышает COMPLAINT_COUNTER, иначе False.
    """
    blacklist = await black_list_check_by_platform_id_or_contact_information(
        db, contact_information=contact_information
    )

    return blacklist and blacklist.complaint_counter >= COMPLAINT_COUNTER
