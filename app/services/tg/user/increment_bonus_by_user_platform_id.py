from models import User
from query_objects.users.get_user_by_platform_id import get_user_by_platform_id
from sqlalchemy.ext.asyncio import AsyncSession


async def increment_bonus_by_user_platform_id(
    user_platform_id: int, session: AsyncSession
) -> User:
    user: User | None = await get_user_by_platform_id(session, user_platform_id)

    if not user:
        raise ValueError(f"Пользователь с id {user_platform_id} не найден")

    user.bonus += 1

    session.add(user)
    await session.commit()
    await session.refresh(user)

    return user
