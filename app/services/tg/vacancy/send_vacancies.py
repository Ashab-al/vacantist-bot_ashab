import asyncio

from aiogram import Bot
from aiogram.types import CallbackQuery
from bot.filters.callback.get_vacancies_callback import GetVacanciesCallback
from bot.keyboards.vacancy_keyboard import vacancy_keyboard
from database import with_session
from lib.tg.common import jinja_render
from models import SentMessage
from models.user import User
from models.vacancy import Vacancy
from sqlalchemy.ext.asyncio import AsyncSession

DELAY = 0.6


@with_session
async def send_vacancies(
    callback: CallbackQuery,
    vacancies: list[Vacancy],
    callback_data: GetVacanciesCallback,
    user: User,
    bot: Bot,
    session: AsyncSession,
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

        result = await bot.send_message(
            chat_id=callback.from_user.id,
            text=await jinja_render("pagination/vacancy", data),
            reply_markup=await vacancy_keyboard(user, vacancy),
        )
        session.add(
            SentMessage(
                user_id=user.id,
                message_id=result.message_id,
                vacancy_id=vacancy.id,
            )
        )
        number += 1
        await asyncio.sleep(DELAY)
    await session.commit()

    return number - 1
