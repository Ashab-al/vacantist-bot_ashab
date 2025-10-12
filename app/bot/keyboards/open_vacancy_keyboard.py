from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup
from bot.keyboards.for_vacancy_spam_button import for_vacancy_spam_button
from bot.keyboards.points_button import points_button
from models.user import User
from models.vacancy import Vacancy

MAX_COUNT_BUTTON_IN_LINE = 1


async def open_vacancy_keyboard(user: User, vacancy: Vacancy) -> InlineKeyboardMarkup:
    """
    Создает клавиатуру для открытой вакансии.

    Args:
        user (User): Пользователь, для которого строится клавиатура.
        vacancy (Vacancy): Вакансия, к которой относится клавиатура.

    Returns:
        InlineKeyboardMarkup: Клавиатура с кнопками.

    Notes:
        - Кнопки выравниваются с максимальным количеством в строке, равным 1.
    """
    kb = InlineKeyboardBuilder()

    kb.add(await points_button(user))
    kb.add(await for_vacancy_spam_button(vacancy))
    kb.adjust(MAX_COUNT_BUTTON_IN_LINE, repeat=True)

    return kb.as_markup()
