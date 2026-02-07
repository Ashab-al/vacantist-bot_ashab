from aiogram import Bot, Router, F
from aiogram.enums.chat_type import ChatType
from aiogram.types import CallbackQuery
from bot.filters.callback.spam_vacancy_callback import (
    SpamVacancyCallback,
)
from database import with_session
from services.tg.vacancy.send_spam_vacancy_in_admin_group import (
    send_spam_vacancy_in_admin_group,
)
from sqlalchemy.ext.asyncio import AsyncSession
from config import settings

router = Router(name="Обработчик логики связанной со спамом")
router.message.filter(
    (F.chat.type == ChatType.PRIVATE) | (F.chat.id == settings.admin_chat_id)
)

@router.callback_query(SpamVacancyCallback.filter())
@with_session
async def reaction_choice_spam_vacancy(
    callback: CallbackQuery,
    callback_data: SpamVacancyCallback,
    session: AsyncSession,
    bot: Bot,
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
    await send_spam_vacancy_in_admin_group(bot, callback_data, callback, session)
