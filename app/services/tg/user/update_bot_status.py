from enums.bot_status_enum import BotStatusEnum
from models.user import User
from sqlalchemy.ext.asyncio import AsyncSession


async def update_bot_status(
    db: AsyncSession, user: User, new_status: BotStatusEnum
) -> User:
    """
    Обновляет статус бота пользователя в базе данных.

    Args:
        db (AsyncSession): Асинхронная сессия SQLAlchemy для работы с базой данных.
        user (User): Объект пользователя, чей статус нужно обновить.
        new_status (BotStatusEnum): Новый статус бота для установки.

    Returns:
        User: Объект пользователя, обновленный в базе данных.

    Raises:
        ValueError: Если пользователь с таким `platform_id` не найден.
    """

    user.bot_status = new_status

    await db.commit()
    await db.refresh(user)

    return user
