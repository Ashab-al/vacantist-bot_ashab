from sqlalchemy.ext.asyncio import AsyncSession
from models.vacancy import Vacancy
from sqlalchemy import (
    select,
    or_
)
from models.blacklist import BlackList


async def black_list_check(
    db: AsyncSession,
    platform_id: str,
    contact_information: str
) -> None:
    blacklist: BlackList | None = (
        await db.scalars(
            select(BlackList).where(
                or_(
                    BlackList.contact_information == contact_information, 
                    BlackList.contact_information == platform_id
                )
            )
        )
    ).one_or_none()

    if blacklist:
        raise ValueError('error.messages.error_validate_vacancy')
    
    