from models.user import User
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from sqlalchemy import select


async def get_user_by_platform_id(
    db: AsyncSession,
    platform_id: int
) -> User | None:
    """Вернуть пользователя по platform_id"""
    return (
        await db.execute(
            select(User).where(User.platform_id==platform_id).options(joinedload(User.categories))
        )
    ).unique().scalars().first()