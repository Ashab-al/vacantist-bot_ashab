from functools import wraps
from services.tg.user.find_or_create_with_update_by_platform_id import find_or_create_with_update_by_platform_id
from models.user import User
from sqlalchemy.ext.asyncio import AsyncSession
from aiogram.types import Message, CallbackQuery


async def current_user(
    session: AsyncSession,
    message: Message = None,
    query: CallbackQuery = None
) -> User:
    """Вернуть текущего пользователя"""
    source = message or query
    
    user = await find_or_create_with_update_by_platform_id(
        db=session,
        user_data=source.from_user    
    )
    return user
