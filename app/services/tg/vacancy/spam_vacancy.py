from lib.tg.constants import SOURCE
from models.blacklist import BlackList
from models.vacancy import Vacancy
from query_objects.blacklist.black_list_check_by_platform_id_and_contact_information import (
    black_list_check_by_platform_id_or_contact_information,
)
from query_objects.vacancies.find_vacancy_by_id import find_vacancy_by_id
from sqlalchemy.ext.asyncio import AsyncSession

COMPLAINT_COUNTER = 1
BLACKLISTED = "blacklisted"
ZERO = 0


async def spam_vacancy(db: AsyncSession, vacancy_id: int) -> str | None:
    """
    Обрабатывает жалобы на вакансию и обновляет черный список.

    Функция проверяет, находится ли вакансия в черном списке по `platform_id` или
    контактной информации. Если записи нет — создаёт новую с нулевым счётчиком жалоб.
    Если количество жалоб превышает `COMPLAINT_COUNTER`, возвращает статус `BLACKLISTED`.
    В противном случае увеличивает счётчик жалоб на 1.

    Args:
        db (AsyncSession): Асинхронная сессия SQLAlchemy.
        vacancy_id (int): ID вакансии, на которую была подана жалоба.

    Returns:
        str: 'blacklisted', если количество жалоб достигло порога, иначе None.
    """
    vacancy: Vacancy = await find_vacancy_by_id(db, vacancy_id)
    contact_information: str = (
        vacancy.platform_id if vacancy.source == SOURCE else vacancy.contact_information
    )

    blacklist: BlackList = await black_list_check_by_platform_id_or_contact_information(
        db, contact_information=contact_information
    )
    if not blacklist:
        blacklist: BlackList = BlackList(
            contact_information=contact_information, complaint_counter=ZERO
        )
        db.add(blacklist)
        await db.commit()
        await db.refresh(blacklist)

    if blacklist.complaint_counter >= COMPLAINT_COUNTER:
        return BLACKLISTED

    blacklist.complaint_counter += 1
    await db.commit()
    await db.refresh(blacklist)
