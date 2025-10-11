from models.user import User
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload


async def get_user_by_id(db: AsyncSession, user_id: int) -> User | None:
    """
    Получить пользователя по его ID с предзагруженными категориями.

    Args:
        db (AsyncSession): Асинхронная сессия SQLAlchemy для работы с базой данных.
        user_id (int): ID пользователя.

    Returns:
        User | None: Пользователь с предзагруженными категориями или None, если не найден.
    """
    return (
        (
            await db.execute(
                select(User)
                .where(User.id == user_id)
                .options(joinedload(User.categories))
            )
        )
        .unique()
        .scalars()
        .first()
    )
