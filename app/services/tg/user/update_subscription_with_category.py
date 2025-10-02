from aiogram.types import CallbackQuery
from aiogram import Bot
from bot.filters.callback.category_callback import CategoryCallback
from repositories.categories.get_category_by_id import get_category_by_id
from sqlalchemy.ext.asyncio import AsyncSession
from models.category import Category
from aiogram.types.user import User as AiogramTgUser
from services.tg.category.find_subscribe import find_subscribe
from models.user import User

async def update_subscription_with_category(
    category_callback: CategoryCallback, 
    db: AsyncSession,
    subscribed_categories: list[Category],
    user: User
) -> dict[str, str]:
    category: Category | None = await get_category_by_id(
        db, 
        category_callback.category_id
    )
    data: dict[str, str] = {"path_to_templates": ""}

    if category is None:
        raise ValueError('Такой категории не найдено')
    
    if category in subscribed_categories:
        user.categories.remove(category)
        data['path_to_templates'] = "unsubscribe"
    else:
        user.categories.append(category)
        data['path_to_templates'] = "subscribe"
    
    
    await db.commit()

    return data
    