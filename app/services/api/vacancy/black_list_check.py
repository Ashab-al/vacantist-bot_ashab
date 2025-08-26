from sqlalchemy.ext.asyncio import AsyncSession
from models.vacancy import Vacancy
from sqlalchemy import (
    select,
)


async def black_list_check(
    db: AsyncSession,
    platform_id: int,
    contact_information: str
) -> Vacancy:
    ...