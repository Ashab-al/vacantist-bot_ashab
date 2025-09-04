from models.user import User
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from sqlalchemy import select


async def get_user_by_id(
    db: AsyncSession,
    user_id: int
) -> User | None:
    """Вернуть пользователя по id"""
    return (
        await db.execute(
            select(User).where(User.id==user_id).options(joinedload(User.categories))
        )
    ).unique().scalars().first()