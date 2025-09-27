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
from models.vacancy import Vacancy
from models.user import User
from bot.filters.callback.open_vacancy_callback import OpenVacancyCallback
from bot.filters.callback.spam_vacancy_callback import SpamVacancyCallback

MAX_COUNT_BUTTON_IN_LINE = 1

async def vacancy_keyboard(
    user: User,
    vacancy: Vacancy
):
    kb = InlineKeyboardBuilder()

    kb.button(
        text=await jinja_render('button/get_contact'),
        callback_data=OpenVacancyCallback(vacancy_id=vacancy.id).pack()
    )
    kb.button(
        text=await jinja_render('button/by_points', {"user": user, "COUNT_FOR_FULL_BATTERY": User.COUNT_FOR_FULL_BATTERY}),
        callback_data=i18n['buttons']['points']
    )
    kb.button(
        text=i18n['buttons']['for_vacancy_message']['spam'],
        callback_data=SpamVacancyCallback(vacancy_id=vacancy.id).pack()
    )
    kb.adjust(MAX_COUNT_BUTTON_IN_LINE, repeat=True)
    
    return kb.as_markup()
