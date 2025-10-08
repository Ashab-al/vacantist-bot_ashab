from models.user import User
from sqlalchemy.ext.asyncio import AsyncSession
from repositories.users.get_user_by_platform_id import get_user_by_platform_id
from aiogram.types.user import User as AiogramTgUser


async def update_points(
    db: AsyncSession,     
    aiogram_user: AiogramTgUser,
    points: int 
) -> None:
    """
    Обновить количество поинтов (`point`) у пользователя

    Args:
        db (AsyncSession): Асинхронная сессия SQLAlchemy для работы с базой данных.
        aiogram_user (AiogramTgUser): Объект пользователя телеграм
        points (int): Количество поинтов на добавление к пользователю
    
    Returns:
        None
    
    Raises:
        ValueError: Пользователь с platform_id `user.platform_id` не найден
    """
    user: User = await get_user_by_platform_id(db, aiogram_user.id)
    
    if user is None:
        raise ValueError(f"Пользователь с platform_id {aiogram_user.id} не найден")

    user.point = user.point + points

    await db.commit()
    await db.refresh(user)

    return user