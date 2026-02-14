from query_objects.blacklist.black_list_check_by_platform_id_and_contact_information import (
    black_list_check_by_platform_id_or_contact_information,
)
from sqlalchemy.ext.asyncio import AsyncSession
from models import BlackList, Vacancy
from asyncio import TaskGroup

async def check_blacklist(db: AsyncSession, vacancy: Vacancy) -> BlackList | None:
    """
    Проверяет, находится ли вакансия в черном списке по `platform_id` или контактной информации.

    Args:
        db (AsyncSession): Асинхронная сессия SQLAlchemy.
        vacancy (Vacancy): Объект вакансии, для которой проверяется наличие в черном списке.

    Returns:
        BlackList | None: Объект BlackList, если вакансия находится в черном списке, иначе None.
    """
    async with TaskGroup() as tg:
        task_by_contact_information = tg.create_task(
            black_list_check_by_platform_id_or_contact_information(
                db, contact_information=vacancy.contact_information
            )
        )
        task_by_platform_id = tg.create_task(
            black_list_check_by_platform_id_or_contact_information(
                db, contact_information=vacancy.platform_id
            )
        )

    return task_by_contact_information.result() or task_by_platform_id.result()
