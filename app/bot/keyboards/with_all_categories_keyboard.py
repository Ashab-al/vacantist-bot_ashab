from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup
from lib.tg.common import jinja_render
from repositories.categories.get_all_categories import get_all_categories
from models.category import Category
from sqlalchemy.ext.asyncio import AsyncSession
from bot.filters.callback.category_callback import CategoryCallback 
from .get_vacancies_button import get_vacancies_button


MAX_COUNT_BUTTON_IN_LINE = 2

async def with_all_categories_keyboard(
    db: AsyncSession,
    subscribed_categories: list[Category]  
) -> InlineKeyboardMarkup:
    """
    Создать и вернуть клавиатуру с категориями и кнопкой для просмотра вакансий.  

    Args:
        db (AsyncSession): Асинхронная сессия SQLAlchemy для работы с базой данных.
        subscribed_categories (list[Category]): Список категорий, на которые пользователь подписан.

    Returns:
        InlineKeyboardMarkup: Объект клавиатуры с кнопками категорий и кнопкой перехода к вакансиям.
    """
    kb = InlineKeyboardBuilder()
    all_categories: list[Category] = await get_all_categories(db)

    for category in all_categories:
        kb.button(
            text=await jinja_render(
                'button/two_button_text', 
                {
                    "category": category, 
                    "subscribed_categories": subscribed_categories
                }
            ),
            callback_data=CategoryCallback(category_id=category.id).pack()
        )
    
    kb.adjust(MAX_COUNT_BUTTON_IN_LINE, repeat=True)

    kb.row(await get_vacancies_button())
    return kb.as_markup()