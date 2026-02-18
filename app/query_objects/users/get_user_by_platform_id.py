from models.sent_message import SentMessage
from models.user import User
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload


async def get_user_by_platform_id(db: AsyncSession, platform_id: int) -> User | None:
    """
    Получить пользователя по его platform_id с предзагруженными категориями.

    Args:
        db (AsyncSession): Асинхронная сессия SQLAlchemy для работы с базой данных.
        platform_id (int): ID пользователя в Telegram.

    Returns:
        User | None: Пользователь с предзагруженными категориями или None, если не найден.
    """
    return (
        (
            await db.execute(
                select(User)
                .where(User.platform_id == platform_id)
                .options(joinedload(User.categories))
            )
        )
        .unique()
        .scalars()
        .first()
    )
