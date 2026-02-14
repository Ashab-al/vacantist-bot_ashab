from query_objects.blacklist.black_list_check_by_platform_id_and_contact_information import (
    black_list_check_by_platform_id_or_contact_information,
)
from sqlalchemy.ext.asyncio import AsyncSession
from models import BlackList, Vacancy
from lib.tg.constants import SOURCE

async def check_blacklist(db: AsyncSession, vacancy: Vacancy) -> BlackList | None:
    """
    Проверяет, находится ли вакансия в черном списке по `platform_id` или контактной информации.

    Args:
        db (AsyncSession): Асинхронная сессия SQLAlchemy.
        vacancy (Vacancy): Объект вакансии, для которой проверяется наличие в черном списке.

    Returns:
        BlackList | None: Объект BlackList, если вакансия находится в черном списке, иначе None.
    """
    contact_information: str = vacancy.contact_information

    if vacancy.source == SOURCE:
        contact_information = vacancy.platform_id

    return await black_list_check_by_platform_id_or_contact_information(
        db, contact_information=contact_information
    )
