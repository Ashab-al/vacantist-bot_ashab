from models.category import User
from repositories.users.get_all_users import get_all_users
from sqlalchemy.ext.asyncio import AsyncSession


async def users_list(
    db: AsyncSession
) -> list[User]:
    users: list[User] = await get_all_users(db)

    return users