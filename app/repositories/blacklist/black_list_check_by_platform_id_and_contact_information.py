from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import (
    select,
    or_
)
from models.blacklist import BlackList


async def black_list_check_by_platform_id_or_contact_information(
    db: AsyncSession,
    platform_id: str | None = None,
    contact_information: str | None = None
) -> BlackList | None:
    """Вернуть информацию есть ли вакансия в черном списке"""
    
    conditions = []
    if platform_id:
        conditions.append(BlackList.contact_information == platform_id)

    if contact_information:
        conditions.append(BlackList.contact_information == contact_information)

    if not conditions:
        raise ValueError("Не передан ни один аргумент")
    result = await db.scalars(
            select(BlackList).where(or_(*conditions))
        )
    print()
    return result.one_or_none()