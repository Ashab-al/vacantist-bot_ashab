import asyncio

from aiogram.types import InlineKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from lib.tg.common import jinja_render


async def menu_keyboard() -> InlineKeyboardMarkup:
    """
    Создает и возвращает клавиатуру главного меню для пользователя.

    Returns:
        InlineKeyboardMarkup: Клавиатура с кнопками главного меню.

    Notes:
        - Кнопки размещаются с максимальной шириной 3 и одной кнопкой на последней линии.
        - Клавиатура возвращается с включенным параметром `resize_keyboard=True`.
    """
    kb = ReplyKeyboardBuilder()

    btns_text = await asyncio.gather(
        jinja_render("menu/button/points"),
        jinja_render("menu/button/advertisement"),
        jinja_render("menu/button/help"),
        jinja_render("menu/button/categories"),
    )

    for text in btns_text:
        kb.add(KeyboardButton(text=text))

    kb.adjust(3, 1)

    return kb.as_markup(resize_keyboard=True)
