from aiogram.filters import BaseFilter
from aiogram.types import Message
from lib.tg.common import jinja_render


class PointsButtonFilter(BaseFilter):
    """
    Фильтр для обработки нажатия кнопки "Поинты" в Telegram.

    Сравнивает текст сообщения пользователя с отрендеренным текстом кнопки
    из Jinja2 шаблона `menu/button/points`.
    """

    async def __call__(self, message: Message) -> bool:
        return message.text == await jinja_render("menu/button/points")
