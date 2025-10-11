from aiogram.types import InlineKeyboardButton
from config import i18n
from lib.tg.common import jinja_render
from models.user import User


async def points_button(user):
    """
    Возвращает объект кнопки 'Поинты' для клавиатуры.
    """
    return InlineKeyboardButton(
        text=await jinja_render(
            "button/by_points",
            {"user": user, "COUNT_FOR_FULL_BATTERY": User.COUNT_FOR_FULL_BATTERY},
        ),
        callback_data=i18n["buttons"]["points"],
    )
