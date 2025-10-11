from aiogram.filters import BaseFilter
from aiogram.types import Message
from lib.tg.common import jinja_render


class CategoryButtonFilter(BaseFilter):
    """
    Фильтр для обработки нажатия кнопки "Категории" в Telegram.

    Сравнивает текст сообщения пользователя с отрендеренным текстом кнопки
    из Jinja2 шаблона `menu/button/categories`.
    """

    async def __call__(self, message: Message) -> bool:
        return message.text == await jinja_render("menu/button/categories")
