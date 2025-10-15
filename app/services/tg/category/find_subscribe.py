from aiogram.types.user import User as AiogramTgUser
from models.category import Category
from models.user import User
from query_objects.users.get_user_by_platform_id import get_user_by_platform_id
from sqlalchemy.ext.asyncio import AsyncSession


async def find_subscribe(
    db: AsyncSession, user_data: AiogramTgUser | User
) -> list[Category]:
    """
    Вернуть список категорий, на которые подписан пользователь `User`

    Args:
        db (AsyncSession): Асинхронная сессия
        user_data (AiogramTgUser | User): Объект AiogramTgUser либо User

    Returns:
        user.categories (list[Category]): Список категорий, на которые подписан пользователь
    """
    platform_id: str | None = None

    if isinstance(user_data, AiogramTgUser):
        platform_id: str = user_data.id

    elif isinstance(user_data, User):
        platform_id: str = user_data.platform_id

    user: User | None = await get_user_by_platform_id(db, platform_id)

    if not user:
        raise ValueError("Пользователь не найден")

    return user.categories
