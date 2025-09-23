from aiogram.types import ReplyKeyboardMarkup, WebAppInfo, InlineKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
import asyncio
from config import settings, i18n
from lib.tg.common import jinja_render
from repositories.categories.get_all_categories import get_all_categories
from models.category import Category
from sqlalchemy.ext.asyncio import AsyncSession
from repositories.categories.get_all_categories import get_all_categories
from bot.filters.callback.category_callback import CategoryCallback 


MAX_COUNT_BUTTON_IN_LINE = 2
VACANCIES_START = "get_vacancies_start_"

async def with_all_categories_keyboard(
    db: AsyncSession,
    subscribed_categories: list[Category]  
) -> InlineKeyboardMarkup:
    """Вернуть кнопки с категориями"""
    kb = InlineKeyboardBuilder()
    all_categories: list[Category] = await get_all_categories(db)
    
    for category in all_categories:
        kb.button(
            text=await jinja_render('button/two_button_text', {"category": category, "subscribed_categories": subscribed_categories}),
            callback_data=CategoryCallback(category_id=category.id).pack()
        )
    
    kb.adjust(MAX_COUNT_BUTTON_IN_LINE, repeat=True)
    
    return kb.as_markup()