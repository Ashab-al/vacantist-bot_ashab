from models.user import User
from sqlalchemy.ext.asyncio import AsyncSession


async def find_or_create_with_update_by_platform_id(
    user_data: dict
) -> User:
    ...