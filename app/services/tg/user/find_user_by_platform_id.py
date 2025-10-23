from exceptions.user_not_found_error import UserNotFoundError
from models.user import User
from query_objects.users.get_user_by_platform_id import get_user_by_platform_id
from sqlalchemy.ext.asyncio import AsyncSession


async def find_user_by_platform_id(db: AsyncSession, platform_id: int) -> User:
    """
    Вернуть пользователя из базы данных по его Telegram `platform_id`.
    Если пользователь с таким `platform_id` не существует, поднимает исключение.

    Args:
        db (AsyncSession): Асинхронная сессия SQLAlchemy для работы с базой данных.
        platform_id (int): Уникальный идентификатор пользователя в Telegram.

    Returns:
        User: Объект пользователя, найденный в базе данных.

    Raises:
        UserNotFoundError: Если пользователь с таким `platform_id` не найден.
    """
    user: User | None = await get_user_by_platform_id(db, platform_id)

    if not user:
        raise UserNotFoundError(platform_id)

    return user
