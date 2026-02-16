from sqlalchemy.ext.asyncio import AsyncSession

from services.tg.spam.add_vacancy_to_blacklist import add_vacancy_to_blacklist
from aiogram import Bot
from aiogram.types import CallbackQuery
from bot.filters.callback.spam_vacancy_callback import (
    SpamVacancyCallbackForAdmin,
)
from lib.tg.common import jinja_render
from services.tg.spam.update_spam_message import update_spam_message

async def admin_confirm_add_vacancy_to_blacklist(
    callback: CallbackQuery,
    callback_data: SpamVacancyCallbackForAdmin,
    session: AsyncSession
) -> None:
    """
    Подтверждает добавление вакансии в черный список.

    Args:
        vacancy_id (int): ID вакансии, которую нужно добавить в черный список.
        db (AsyncSession): Асинхронная сессия SQLAlchemy для взаимодействия с базой данных.

    Returns:
        None
    """

    try:
        await add_vacancy_to_blacklist(callback_data.vacancy_id, session)
    except ValueError as e:

        await callback.message.answer(f"Ошибка: {e}")
        return

    await update_spam_message(
        callback,
        "spam/update_spam_message_in_admin_group"
    )
