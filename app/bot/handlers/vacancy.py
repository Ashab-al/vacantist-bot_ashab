"""Модуль работы с Telegram-ботом через aiogram."""

from aiogram import Bot, Router
from aiogram.types import CallbackQuery
from bot.filters.callback.open_vacancy_callback import OpenVacancyCallback
from bot.filters.callback.spam_vacancy_callback import SpamVacancyCallback
from bot.keyboards.open_vacancy_keyboard import open_vacancy_keyboard
from database import with_session
from enums.check_vacancy_enum import CheckVacancyEnum
from lib.tg.common import jinja_render
from services.tg.open_vacancy import open_vacancy
from services.tg.spam_vacancy import BLACKLISTED, spam_vacancy
from services.tg.user.find_user_by_platform_id import find_user_by_platform_id
from sqlalchemy.ext.asyncio import AsyncSession

router = Router(name="Обработчик вакансий")


@router.callback_query(OpenVacancyCallback.filter())
@with_session
async def reaction_choice_vacancy(
    callback: CallbackQuery,
    callback_data: OpenVacancyCallback,
    session: AsyncSession,
    bot: Bot,
):
    """
    Обрабатывает нажатие на кнопку открытия вакансии в Telegram-боте.

    Функция:
    - Определяет текущего пользователя по данным callback-запроса.
    - Получает данные о вакансии через сервис `open_vacancy`.
    - В зависимости от статуса вакансии:
        * Если статус `WARNING` — показывает пользователю alert с предупреждением.
        * Если статус `OPEN_VACANCY` — редактирует сообщение
        и показывает подробности вакансии с кнопками действий.

    Args:
        callback (CallbackQuery): Объект колбэка Telegram, вызванного при нажатии кнопки.
        callback_data (OpenVacancyCallback): Данные,
            переданные вместе с callback (в том числе ID вакансии).
        session (AsyncSession): Асинхронная сессия для работы с базой данных.
        bot (Bot): Экземпляр Telegram-бота для взаимодействия с пользователем.

    Returns:
        None
    """
    user = await find_user_by_platform_id(session, callback.from_user.id)
    vacancy_data: dict = await open_vacancy(session, user, callback_data.vacancy_id)
    alert_data: dict = {}
    if vacancy_data.get("status") == CheckVacancyEnum.WARNING:
        alert_data["text"] = await jinja_render(
            vacancy_data["path_view"], {"open_vacancy": vacancy_data, "user": user}
        )
        alert_data["show_alert"] = True

    await callback.answer(**alert_data)

    if vacancy_data.get("status") == CheckVacancyEnum.OPEN_VACANCY:
        await bot.edit_message_text(
            chat_id=callback.from_user.id,
            message_id=callback.message.message_id,
            text=await jinja_render(
                vacancy_data.get("path_view"),
                {"open_vacancy": vacancy_data, "user": user},
            ),
            reply_markup=await open_vacancy_keyboard(
                user=user, vacancy=vacancy_data.get("vacancy")
            ),
        )


@router.callback_query(SpamVacancyCallback.filter())
@with_session
async def reaction_choice_spam_vacancy(
    callback: CallbackQuery, callback_data: SpamVacancyCallback, session: AsyncSession
):
    """
    Обрабатывает нажатие на кнопку «Спам» в Telegram-боте.

    Функция:
    - Получает данные о вакансии, на которую пользователь пожаловался.
    - Вызывает сервис `spam_vacancy` для обработки жалобы
    и возможного добавления вакансии в чёрный список.
    - Отправляет пользователю alert с результатом действия
    (например, "вакансия добавлена в список спама").

    Args:
        callback (CallbackQuery): Объект Telegram callback-запроса, вызванного при нажатии кнопки.
        callback_data (SpamVacancyCallback): Данные, переданные вместе с callback
        (включая ID вакансии).
        session (AsyncSession): Асинхронная сессия SQLAlchemy для взаимодействия с базой данных.

    Returns:
        None
    """
    await callback.answer(
        await jinja_render(
            "callback_query/spam_vacancy",
            {
                "outcome": await spam_vacancy(session, callback_data.vacancy_id),
                "BLACKLISTED": BLACKLISTED,
            },
        ),
        show_alert=True,
    )
