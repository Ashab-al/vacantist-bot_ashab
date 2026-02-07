"""Модуль работы с Telegram-ботом через aiogram."""

from aiogram import Bot, F, Router
from aiogram.types import CallbackQuery
from aiogram.enums.chat_type import ChatType
from bot.filters.callback.get_vacancies_callback import GetVacanciesCallback
from bot.keyboards.get_more_vacancies_keyboard import get_more_vacancies_keyboard
from database import with_session
from lib.tg.common import jinja_render
from services.tg.vacancy.vacancies_pagination import vacancies_pagination
from sqlalchemy.ext.asyncio import AsyncSession

router = Router(name="Обработчик пагинации вакансий")
router.message.filter(F.chat.type == ChatType.PRIVATE)


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
        - Получает текущего пользователя через `find_user_by_platform_id`.
        - Извлекает вакансии недели через `fetch_vacancies_for_the_week`.
        - Проверяет статус выборки вакансий и уведомляет пользователя, если нет данных.
        - Отправляет вакансии пользователю с задержкой DELAY между сообщениями.
        - Прикрепляет клавиатуру для получения следующей страницы вакансий.
    """
    user, number, next_page, count = await vacancies_pagination(
        callback, callback_data, session, bot
    )
    await bot.send_message(
        chat_id=callback.from_user.id,
        text=await jinja_render(
            "pagination/sended_vacancies",
            {"number": number, "count": count},
        ),
        reply_markup=await get_more_vacancies_keyboard(user=user, page=next_page),
    )
