from aiogram.utils.keyboard import InlineKeyboardBuilder
from config import i18n
from lib.tg.common import jinja_render
from models.vacancy import Vacancy
from models.user import User
from bot.filters.callback.spam_vacancy_callback import SpamVacancyCallback

MAX_COUNT_BUTTON_IN_LINE = 1

async def open_vacancy_keyboard(
    user: User,
    vacancy: Vacancy
):
    kb = InlineKeyboardBuilder()

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
