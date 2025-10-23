from enums.bot_status_enum import BotStatusEnum
from models.user import User
from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession


async def update_users_bot_status(
    db: AsyncSession, blocked_user_ids: list[int]
) -> None:
    """
    Обновить `bot_status` на `BOT_BLOCKED` у пользователей

    Args:
        db (AsyncSession): Асинхронная сессия SQLAlchemy для работы с базой данных.
        blocked_user_ids (list[int]): Список id пользователей
    """
    await db.execute(
        (
            update(User)
            .where(User.id.in_(blocked_user_ids))
            .values(bot_status=BotStatusEnum.BOT_BLOCKED)
        )
    )
    await db.commit()
