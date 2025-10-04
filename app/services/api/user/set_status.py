from sqlalchemy.ext.asyncio import AsyncSession
from schemas.api.users.set_status.request import SetStatusUserIdRequest, SetStatusRequest
from models.user import User
from services.api.user.find_user_by_id import find_user_by_id


async def set_status(
    db: AsyncSession,
    user_id: SetStatusUserIdRequest,
    bot_status: SetStatusRequest
) -> User:
    """
    Обновляет статус (`bot_status`) у пользователя

    Args:
        db (AsyncSession): Асинхронная сессия SQLAlchemy для работы с базой данных
        user_id (SetStatusUserIdRequest): Схема для поиска пользователя
        bot_status (SetStatusRequest): Схема для обновления `bot_status` у пользователя
    
    Returns:
        User: Объект пользователя
    """
    user: User = await find_user_by_id(db, user_id)
    
    user.bot_status = bot_status.bot_status

    db.add(user)
    await db.commit()
    await db.refresh(user)
    
    return user