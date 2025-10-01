from aiogram.types import InlineKeyboardButton
from lib.tg.common import jinja_render
from bot.filters.callback.get_vacancies_callback import GetVacanciesCallback

PAGE = 1
PAGE_SIZE = 3

async def get_vacancies_button(
    page: int = PAGE,
    page_size: int = PAGE_SIZE
) -> InlineKeyboardButton:
    """Кнопка для пагинации вакансий"""
    return InlineKeyboardButton(
        text=await jinja_render('button/get_vacancies'),
        callback_data=GetVacanciesCallback(page=page, page_size=page_size).pack()
    )
