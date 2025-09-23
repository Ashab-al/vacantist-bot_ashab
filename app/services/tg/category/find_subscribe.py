from models.user import User
from sqlalchemy.ext.asyncio import AsyncSession
from aiogram.types.user import User as AiogramTgUser
from repositories.users.get_user_by_platform_id import get_user_by_platform_id
from models.category import Category

async def find_subscribe(
    db: AsyncSession,
    user_data: AiogramTgUser
) -> list[Category]:
    user: User | None = await get_user_by_platform_id(
        db,
        user_data.id
    )
    return user.categories

