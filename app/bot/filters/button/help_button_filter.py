from aiogram.filters import BaseFilter
from aiogram.types import Message
from lib.tg.common import jinja_render


class HelpButtonFilter(BaseFilter):
    """Фильтр для кнопки help"""
    async def __call__(self, message: Message) -> bool:
       return message.text == await jinja_render('menu/button/help')