from aiogram.types import InlineKeyboardButton
from bot.filters.callback.spam_vacancy_callback import SpamVacancyCallback
from config import i18n
from models.vacancy import Vacancy


async def for_vacancy_spam_button(vacancy: Vacancy):
    """
    Возвращает объект кнопки 'Спам' для клавиатуры.
    """
    return InlineKeyboardButton(
        text=i18n["buttons"]["for_vacancy_message"]["spam"],
        callback_data=SpamVacancyCallback(vacancy_id=vacancy.id).pack(),
    )
