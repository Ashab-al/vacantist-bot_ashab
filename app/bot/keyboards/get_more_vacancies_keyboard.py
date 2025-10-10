from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from bot.filters.callback.get_vacancies_callback import GetVacanciesCallback
from bot.keyboards.get_vacancies_button import PAGE_SIZE
from config import i18n
from lib.tg.common import jinja_render
from models.user import User

MAX_COUNT_BUTTON_IN_LINE = 1


async def get_more_vacancies_keyboard(user: User, page: int) -> InlineKeyboardButton:
    """
    Создает inline-клавиатуру для получения следующей страницы вакансий.

    Args:
        user (User): Текущий пользователь, используется для персонализации кнопки по бонусам.
        page (int): Номер следующей страницы вакансий.

    Returns:
        InlineKeyboardButton: Inline-клавиатура.

    Notes:
        - Количество кнопок в строке регулируется константой `MAX_COUNT_BUTTON_IN_LINE`.
    """
    kb = InlineKeyboardBuilder()
    kb.button(
        text=await jinja_render("pagination/get_more_vacancies"),
        callback_data=GetVacanciesCallback(page=page, page_size=PAGE_SIZE).pack(),
    )
    kb.button(
        text=await jinja_render(
            "button/by_points",
            {"user": user, "COUNT_FOR_FULL_BATTERY": User.COUNT_FOR_FULL_BATTERY},
        ),
        callback_data=i18n["buttons"]["points"],
    )

    kb.adjust(MAX_COUNT_BUTTON_IN_LINE, repeat=True)

    return kb.as_markup()
