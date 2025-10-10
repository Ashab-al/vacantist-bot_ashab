from models.user import User
from schemas.api.users.set_bonus.request import (SetBonusRequest,
                                                 SetBonusUserIdRequest)
from services.api.user.find_user_by_id import find_user_by_id
from sqlalchemy.ext.asyncio import AsyncSession


async def set_bonus(
    db: AsyncSession, user_id: SetBonusUserIdRequest, bonus: SetBonusRequest
) -> User:
    """
    Обновляет количество бонусов у пользователя

    Args:
        db (AsyncSession): Асинхронная сессия SQLAlchemy для работы с базой данных
        user_id (SetBonusUserIdRequest): Схема для поиска пользователя
        bonus (SetBonusRequest): Схема для обновления количество бонусов у пользователя

    Returns:
        User: Объект пользователя
    """
    user: User = await find_user_by_id(db, user_id)

    user.bonus = bonus.count

    db.add(user)
    await db.commit()
    await db.refresh(user)

    return user
