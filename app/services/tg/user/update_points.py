from models.user import User
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from schemas.tg.user.tg_user import TgUser
from repositories.users.get_user_by_platform_id import get_user_by_platform_id
from aiogram.types.user import User as AiogramTgUser
from repositories.users.get_user_by_platform_id import get_user_by_platform_id


async def update_points(
    db: AsyncSession,     
    aiogram_user: AiogramTgUser,
    points: int 
):
    user: User = await get_user_by_platform_id(db, aiogram_user.id)
    
    if user is None:
        raise ValueError(f"Пользователь с platform_id {user_platform_id} не найден")

    user.point = user.point + points

    await db.commit()
    await db.refresh(user)

    return user