from models.blacklist import BlackList
from models.vacancy import Vacancy
from query_objects.vacancies.find_vacancy_by_id import find_vacancy_by_id
from sqlalchemy.ext.asyncio import AsyncSession
from services.tg.spam.check_blacklist import check_blacklist


COMPLAINT_COUNTER = 1

async def add_vacancy_to_blacklist(
    vacancy_id: int,
    db: AsyncSession
) -> None:
    """
    Добавляет вакансию в черный список.

    Args:
        vacancy_id (int): ID вакансии, которую нужно добавить в черный список.
        session (AsyncSession): Асинхронная сессия SQLAlchemy для взаимодействия с базой данных.

    Returns:
        None
    """
    vacancy: Vacancy | None = await find_vacancy_by_id(db, vacancy_id)

    if vacancy is None:
        raise ValueError(f"Вакансия с ID {vacancy_id} не найдена")

    if await check_blacklist(db, vacancy):
        raise ValueError(f"Вакансия с контактной информацией {vacancy.contact_information} уже в черном списке")

    new_blacklist: BlackList = BlackList(
        contact_information=vacancy.contact_information, complaint_counter=COMPLAINT_COUNTER
    )
    db.add(new_blacklist)
    await db.commit()
    await db.refresh(new_blacklist)
