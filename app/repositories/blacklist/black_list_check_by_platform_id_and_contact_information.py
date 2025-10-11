from models.blacklist import BlackList
from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession


async def black_list_check_by_platform_id_or_contact_information(
    db: AsyncSession,
    platform_id: str | None = None,
    contact_information: str | None = None,
) -> BlackList | None:
    """
    Проверить, есть ли запись о вакансии в черном списке по platform_id или contact_information.

    Args:
        db (AsyncSession): Асинхронная сессия SQLAlchemy для работы с базой данных.
        platform_id (str | None): ID пользователя/отправителя вакансии.
        contact_information (str | None): Контактная информация из вакансии.

    Returns:
        BlackList | None: Объект BlackList, если найден, иначе None.

    Raises:
        ValueError: Если не передан ни один из аргументов.
    """

    conditions = []
    if platform_id:
        conditions.append(BlackList.contact_information == platform_id)

    if contact_information:
        conditions.append(BlackList.contact_information == contact_information)

    if not conditions:
        raise ValueError("Не передан ни один аргумент")
    result = await db.scalars(select(BlackList).where(or_(*conditions)))

    return result.one_or_none()
