from aiogram.types.user import User as TgUser
from exceptions.user_not_found_error import UserNotFoundError
from models.user import User
from services.tg.send_analytics import send_analytics
from services.tg.user import create_user, find_user_by_platform_id
from sqlalchemy.ext.asyncio import AsyncSession


async def find_or_create_user_with_analytics(
    session: AsyncSession, from_user: TgUser
) -> User:
    """
    Получает пользователя по platform_id или создает нового, если пользователь не найден.
    Args:
        session (AsyncSession): Асинхронная сессия SQLAlchemy для работы с базой данных.
        from_user (TgUser): Объект пользователя Telegram (aiogram.types.User).
    """
    try:
        user: User = await find_user_by_platform_id(session, from_user.id)
    except UserNotFoundError:
        user = await create_user(session, from_user)
        await send_analytics(session, user)

    return user
