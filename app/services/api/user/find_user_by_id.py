from models.user import User
from repositories.users.get_user_by_id import get_user_by_id
from schemas.api.users.show.request import ShowUserRequest
from sqlalchemy.ext.asyncio import AsyncSession


async def find_user_by_id(db: AsyncSession, user_id: ShowUserRequest) -> User:
    """
    Возвращает пользователя по `id`

    Args:
        db (AsyncSession): Асинхронная сессия SQLAlchemy для работы с базой данных
        user_id (ShowUserRequest): Схема для поиска пользователя

    Returns:
        User: Объект пользователя

    Raises:
        ValueError: Пользователя по `id` - `user_id.id` нет в базе
    """
    user: User | None = await get_user_by_id(db, user_id.id)

    if not user:
        raise ValueError(f"Пользователя по id - {user_id.id} нет в базе")

    return user
