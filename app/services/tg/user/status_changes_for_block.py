from models.user import User
from sqlalchemy.ext.asyncio import AsyncSession
from repositories.users.get_user_by_platform_id import get_user_by_platform_id
from aiogram.types.user import User as AiogramTgUser
from enums.bot_status_enum import BotStatusEnum


async def status_changes_for_block(
    db: AsyncSession,
    user_data: AiogramTgUser
) -> User:
    """
    Изменить статус пользователя `user.bot_status` на `BOT_BLOCKED`

    Args:
        db (AsyncSession): Асинхронная сессия SQLAlchemy для работы с базой данных.
        user_data (AiogramTgUser): Объект пользователя телеграм
    
    Returns:
        User: Пользователь с обновленным bot_status
    
    Raises:
        ValueError: Пользователь не найден в базе `user_data`
    """
    user: User = await get_user_by_platform_id(
        db,
        user_data.id
    )
    
    if user is None:
        raise ValueError(f"Пользователь не найден в базе {user_data}")
    
    user.bot_status = BotStatusEnum.BOT_BLOCKED

    await db.commit()
    await db.refresh(user)

    return user