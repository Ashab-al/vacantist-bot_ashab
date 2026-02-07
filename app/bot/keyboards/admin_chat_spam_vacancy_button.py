from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup
from lib.tg.common import jinja_render
from bot.filters.callback.spam_vacancy_callback import SpamVacancyCallbackForAdmin

MAX_COUNT_BUTTON_IN_LINE = 1


def admin_chat_spam_vacancy_button(
    spam_vacancy: SpamVacancyCallbackForAdmin
) -> InlineKeyboardMarkup:

    kb = InlineKeyboardBuilder()

    kb.button(
        text="Подтвердить спам",
        callback_data=spam_vacancy.pack(),
    )
    kb.adjust(MAX_COUNT_BUTTON_IN_LINE, repeat=True)

    return kb.as_markup()
