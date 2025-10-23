from aiogram.types.user import User as AiogramTgUser
from models.user import User
from services.tg.user.find_user_by_platform_id import find_user_by_platform_id
from sqlalchemy.ext.asyncio import AsyncSession


async def update_points(
    db: AsyncSession, aiogram_user: AiogramTgUser, points: int
) -> None:
    """
    Обновить количество поинтов (`point`) у пользователя

    Args:
        db (AsyncSession): Асинхронная сессия SQLAlchemy для работы с базой данных.
        aiogram_user (AiogramTgUser): Объект пользователя телеграм
        points (int): Количество поинтов на добавление к пользователю

    Returns:
        None
    """
    user: User = await find_user_by_platform_id(db, aiogram_user.id)

    user.point = user.point + points

    await db.commit()
    await db.refresh(user)

    return user
