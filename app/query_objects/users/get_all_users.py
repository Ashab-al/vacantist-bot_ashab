from models.user import User
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload


async def get_all_users(db: AsyncSession) -> list[User]:
    """
    Получить всех пользователей с предзагруженными категориями.

    Args:
        db (AsyncSession): Асинхронная сессия SQLAlchemy для работы с базой данных.

    Returns:
        list[User]: Список всех пользователей с загруженными категориями.
    """
    users: list[User] = (
        (await db.execute(select(User).options(joinedload(User.categories))))
        .unique()
        .scalars()
        .all()
    )

    return users
