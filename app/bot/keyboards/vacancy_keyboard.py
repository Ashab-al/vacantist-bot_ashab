from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup
from bot.filters.callback.open_vacancy_callback import OpenVacancyCallback
from bot.keyboards.for_vacancy_spam_button import for_vacancy_spam_button
from bot.keyboards.points_button import points_button
from lib.tg.common import jinja_render
from models.user import User
from models.vacancy import Vacancy

MAX_COUNT_BUTTON_IN_LINE = 1


async def vacancy_keyboard(user: User, vacancy: Vacancy) -> InlineKeyboardMarkup:
    """
    Создает inline-клавиатуру для взаимодействия с вакансией.

    Args:
        user (User): Пользователь, для которого строится клавиатура.
        vacancy (Vacancy): Вакансия, к которой относится клавиатура.

    Returns:
        InlineKeyboardMarkup: Клавиатура с кнопками:
            - Получить контактные данные вакансии.
            - Пополнить очки пользователя.
            - Пожаловаться на вакансию (спам).

    Notes:
        Кнопки выстраиваются в одну колонку (по одной в строке).
    """
    kb = InlineKeyboardBuilder()

    kb.button(
        text=await jinja_render("button/get_contact"),
        callback_data=OpenVacancyCallback(vacancy_id=vacancy.id).pack(),
    )
    kb.add(await points_button(user))
    kb.add(await for_vacancy_spam_button(vacancy))
    kb.adjust(MAX_COUNT_BUTTON_IN_LINE, repeat=True)

    return kb.as_markup()
