from aiogram.types import InlineKeyboardButton
from bot.filters.callback.get_vacancies_callback import GetVacanciesCallback
from lib.tg.common import jinja_render

PAGE = 1
PAGE_SIZE = 3


async def get_vacancies_button(
    page: int = PAGE, page_size: int = PAGE_SIZE
) -> InlineKeyboardButton:
    """
    Создает inline-кнопку для получения вакансий с пагинацией.

    Args:
        page (int, optional): Номер страницы вакансий. По умолчанию `PAGE`.
        page_size (int, optional): Количество вакансий на странице. По умолчанию `PAGE_SIZE`.

    Returns:
        InlineKeyboardButton: Кнопка, при нажатии которой бот отправляет вакансии
        согласно указанной странице и размеру страницы.

    Notes:
        - Callback-данные содержат информацию о странице и размере страницы.
    """
    return InlineKeyboardButton(
        text=await jinja_render("button/get_vacancies"),
        callback_data=GetVacanciesCallback(page=page, page_size=page_size).pack(),
    )
