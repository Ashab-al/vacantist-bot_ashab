from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup
from lib.tg.common import jinja_render

MAX_COUNT_BUTTON_IN_LINE = 1
EMOJI_ID = "5445353829304387411"
BUTTON_STYLE = "success"


async def payment_link_button(link: str) -> InlineKeyboardMarkup:
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
        text=await jinja_render("button/payment/to_pay"),
        url=link,
        style=BUTTON_STYLE,
        icon_custom_emoji_id=EMOJI_ID,
    )
    kb.adjust(MAX_COUNT_BUTTON_IN_LINE, repeat=True)

    return kb.as_markup()
