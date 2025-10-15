from models.blacklist import BlackList
from query_objects.blacklist.black_list_check_by_platform_id_and_contact_information import (
    black_list_check_by_platform_id_or_contact_information,
)
from sqlalchemy.ext.asyncio import AsyncSession


async def black_list_check(
    db: AsyncSession, platform_id: str, contact_information: str
) -> None:
    """
    Проверить, находится ли вакансия в черном списке по `platform_id` или контактной информации.

    Args:
        db (AsyncSession): Асинхронная сессия SQLAlchemy для работы с базой данных
        platform_id (str): `id` из телеграм отправителя вакансии
        contact_information (str): Контактная информация из вакансии

    Raises:
        ValueError: Вакансия в черном списке
    """
    blacklist: BlackList | None = (
        await black_list_check_by_platform_id_or_contact_information(
            db, platform_id=platform_id, contact_information=contact_information
        )
    )

    if blacklist:
        raise ValueError("Вакансия в черном списке")
