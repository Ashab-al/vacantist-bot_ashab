from aiogram import Bot
from aiogram.types import CallbackQuery
from bot.filters.callback.get_vacancies_callback import GetVacanciesCallback
from enums.vacancies_for_the_week_enum import VacanciesForTheWeekStatusEnum
from lib.tg.common import jinja_render
from models.user import User
from services.tg.user.find_user_by_platform_id import find_user_by_platform_id
from services.tg.vacancy.send_vacancies import send_vacancies
from services.tg.vacancy.vacancies_for_the_week import fetch_vacancies_for_the_week
from sqlalchemy.ext.asyncio import AsyncSession


async def vacancies_pagination(
    callback: CallbackQuery,
    callback_data: GetVacanciesCallback,
    session: AsyncSession,
    bot: Bot,
) -> tuple[User, int, int, int]:
    """
    Обрабатывает пагинацию вакансий для Telegram-бота.

    Args:
        callback (CallbackQuery): Объект callback-запроса.
        callback_data (GetVacanciesCallback): Данные выбранной страницы и размера страницы.
        session (AsyncSession): Асинхронная сессия SQLAlchemy.
        bot (Bot): Экземпляр бота Aiogram.

    Returns:
        tuple(User, int, int, int): Кортеж, содержащий:
            - user (User): Текущий пользователь.
            - number (int): Номер последней отправленной вакансии.
            - next_page (int): Номер следующей страницы.
            - count (int): Общее количество найденных вакансий.
    """
    user: User = await find_user_by_platform_id(session, callback.from_user.id)
    vacancies_for_the_week = await fetch_vacancies_for_the_week(
        session, user, callback_data.page, callback_data.page_size
    )
    next_page: int = 0
    if vacancies_for_the_week.get("status") != VacanciesForTheWeekStatusEnum.OK:
        await callback.answer(
            text=await jinja_render(
                f"pagination/{vacancies_for_the_week.get('status').value}"
            ),
            show_alert=True,
        )
        return

    if callback_data.page <= vacancies_for_the_week["meta"]["max_pages"]:
        next_page = callback_data.page + 1

    number: int = await send_vacancies(
        callback, vacancies_for_the_week.get("items"), callback_data, user, bot
    )
    return user, number, next_page, vacancies_for_the_week["meta"]["count"]
