"""Модуль работы с Telegram-ботом через aiogram."""
import asyncio

from aiogram import Bot, F, Router
from aiogram.types import CallbackQuery
from bot.filters.callback.get_vacancies_callback import GetVacanciesCallback
from bot.keyboards.get_more_vacancies_keyboard import \
    get_more_vacancies_keyboard
from bot.keyboards.vacancy_keyboard import vacancy_keyboard
from database import with_session
from enums.vacancies_for_the_week_enum import VacanciesForTheWeekStatusEnum
from lib.tg.common import jinja_render
from models.user import User
from models.vacancy import Vacancy
from services.tg.user.current_user import current_user
from services.tg.vacancy.vacancies_for_the_week import \
    fetch_vacancies_for_the_week
from sqlalchemy.ext.asyncio import AsyncSession

DELAY = 0.6

router = Router(name="Обработчик пагинации вакансий")
router.message.filter(F.chat.type == "private")


@router.callback_query(GetVacanciesCallback.filter())
@with_session
async def reaction_get_vacancies(
    callback: CallbackQuery,
    callback_data: GetVacanciesCallback,
    session: AsyncSession,
    bot: Bot,
):
    """
    Обрабатывает callback-запрос для получения вакансий с пагинацией.

    Args:
        callback (CallbackQuery): Объект callback-запроса.
        callback_data (GetVacanciesCallback): Данные выбранной страницы и размера страницы.
        session (AsyncSession): Асинхронная сессия SQLAlchemy.
        bot (Bot): Экземпляр бота Aiogram.

    Notes:
        - Получает текущего пользователя через `current_user`.
        - Извлекает вакансии недели через `fetch_vacancies_for_the_week`.
        - Проверяет статус выборки вакансий и уведомляет пользователя, если нет данных.
        - Отправляет вакансии пользователю с задержкой DELAY между сообщениями.
        - Прикрепляет клавиатуру для получения следующей страницы вакансий.
    """
    user: User = await current_user(session, query=callback)
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
    await bot.send_message(
        chat_id=callback.from_user.id,
        text=await jinja_render(
            "pagination/sended_vacancies",
            {"number": number, "count": vacancies_for_the_week["meta"]["count"]},
        ),
        reply_markup=await get_more_vacancies_keyboard(user=user, page=next_page),
    )


async def send_vacancies(
    callback: CallbackQuery,
    vacancies: list[Vacancy],
    callback_data: GetVacanciesCallback,
    user: User,
    bot: Bot,
) -> int:
    """
    Отправляет список вакансий пользователю с нумерацией и клавиатурой.

    Args:
        callback (CallbackQuery): Объект callback-запроса.
        vacancies (list[Vacancy]): Список вакансий для отправки.
        callback_data (GetVacanciesCallback): Данные текущей страницы и размера страницы.
        user (User): Текущий пользователь.
        bot (Bot): Экземпляр бота Aiogram.

    Returns:
        int: Номер последней отправленной вакансии.

    Notes:
        - Использует шаблон Jinja2 для форматирования каждого сообщения.
        - Прикрепляет к каждой вакансии клавиатуру `vacancy_keyboard`.
        - Между отправкой сообщений делает задержку DELAY.
    """
    number: int = ((callback_data.page - 1) * callback_data.page_size) + 1

    for vacancy in vacancies:
        data: dict[str, object] = {"vacancy": vacancy, "number": number, "user": user}

        await bot.send_message(
            chat_id=callback.from_user.id,
            text=await jinja_render("pagination/vacancy", data),
            reply_markup=await vacancy_keyboard(user, vacancy),
        )
        number += 1
        await asyncio.sleep(DELAY)

    return number - 1
