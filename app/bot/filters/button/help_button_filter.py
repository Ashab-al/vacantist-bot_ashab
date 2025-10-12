from aiogram.filters import BaseFilter
from aiogram.types import Message
from lib.tg.common import jinja_render


class HelpButtonFilter(BaseFilter):
    """
    Фильтр для обработки нажатия кнопки "Помощь" в Telegram.

    Сравнивает текст сообщения пользователя с отрендеренным текстом кнопки
    из Jinja2 шаблона `menu/button/help`.
    """

    async def __call__(self, message: Message) -> bool:
        return message.text == await jinja_render("menu/button/help")
