"""Модуль работы с Telegram-ботом через aiogram."""

from aiogram import Bot, Router, F
from aiogram.types import CallbackQuery
from bot.filters.callback.open_vacancy_callback import OpenVacancyCallback
from aiogram.enums.chat_type import ChatType
from bot.keyboards.open_vacancy_keyboard import open_vacancy_keyboard
from database import with_session
from enums.check_vacancy_enum import CheckVacancyEnum
from lib.tg.common import jinja_render
from services.tg.vacancy.open_vacancy_and_show_alert import open_vacancy_and_show_alert
from sqlalchemy.ext.asyncio import AsyncSession

router = Router(name="Обработчик вакансий")
router.message.filter(F.chat.type == ChatType.PRIVATE)

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
    vacancy_data, user = await open_vacancy_and_show_alert(
        callback, callback_data, session
    )
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
