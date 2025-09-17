from aiogram.types import ReplyKeyboardMarkup, WebAppInfo, InlineKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
import asyncio
from config import settings, i18n
from lib.tg.common import jinja_render

def main_keyboard(user_id: int, first_name: str) -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    url_applications = f"{settings.BASE_SITE}/applications?user_id={user_id}"
    url_add_application = f'{settings.BASE_SITE}/form?user_id={user_id}&first_name={first_name}'
    kb.button(text="🌐 Мои заявки", web_app=WebAppInfo(url=url_applications))
    kb.button(text="📝 Оставить заявку", web_app=WebAppInfo(url=url_add_application))
    kb.button(text="ℹ️ О нас")
    if user_id == settings.admin_id:
        kb.button(text="🔑 Админ панель")
    kb.adjust(1)
    return kb.as_markup(resize_keyboard=True)


def back_keyboard() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="🔙 Назад")
    kb.adjust(1)
    return kb.as_markup(resize_keyboard=True)


def admin_keyboard(user_id: int) -> InlineKeyboardMarkup:
    url_applications = f"{settings.BASE_SITE}/admin?admin_id={user_id}"
    kb = InlineKeyboardBuilder()
    kb.button(text="🏠 На главную", callback_data="back_home")
    kb.button(text="📝 Смотреть заявки", web_app=WebAppInfo(url=url_applications))
    kb.adjust(1)
    return kb.as_markup()


def app_keyboard(user_id: int, first_name: str) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    url_add_application = f'{settings.BASE_SITE}/form?user_id={user_id}&first_name={first_name}'
    kb.button(text="📝 Оставить заявку", web_app=WebAppInfo(url=url_add_application))
    kb.adjust(1)
    return kb.as_markup()

async def menu_keyboard() -> InlineKeyboardMarkup:
    """Вернуть кнопки для главного меню"""
    kb = ReplyKeyboardBuilder()
    
    btns_text = await asyncio.gather(
        jinja_render('menu/button/points'), 
        jinja_render('menu/button/advertisement'),
        jinja_render('menu/button/help'),
        jinja_render('menu/button/categories')
    )
    
    for text in btns_text:
        kb.add(KeyboardButton(text=str(text)))
    
    kb.adjust(3, 1)
    
    return kb.as_markup(resize_keyboard=True)