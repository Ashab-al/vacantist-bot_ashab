from aiogram.filters import BaseFilter
from aiogram.types import Message
from lib.tg.common import jinja_render


class CategoryButtonFilter(BaseFilter):
    """Фильтр для кнопки категории"""
    async def __call__(self, message: Message) -> bool:
       return message.text == await jinja_render('menu/button/categories')