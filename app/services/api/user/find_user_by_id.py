from schemas.api.users.show.request import ShowUserRequest
from models.user import User
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from sqlalchemy import select
from repositories.users.get_user_by_id import get_user_by_id


async def find_user_by_id(
    db: AsyncSession,
    user_id: ShowUserRequest
) -> User:
    user: User | None = await get_user_by_id(
        db,
        user_id.id
    )

    if not user:
        raise ValueError(f"Пользователя по id - {user_id.id} нет в базе")

    return user