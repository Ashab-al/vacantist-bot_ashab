from aiogram.types.user import User as AiogramTgUser
from models.category import Category
from models.user import User
from services.tg.user.find_user_by_platform_id import find_user_by_platform_id
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
    platform_id: int | None = None

    if isinstance(user_data, AiogramTgUser):
        platform_id: int = int(user_data.id)

    elif isinstance(user_data, User):
        platform_id: int = int(user_data.platform_id)

    user: User = await find_user_by_platform_id(db, platform_id)

    return user.categories
