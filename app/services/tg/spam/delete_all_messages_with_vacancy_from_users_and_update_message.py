from aiogram.types import CallbackQuery
from bot.filters.callback.spam_vacancy_callback import (
    NotSpamButDeleteMessagesForSpamVacancyCallback,
)
from services.tg.spam.delete_all_messages_with_vacancy_from_users import (
    delete_all_messages_with_vacancy_from_users,
)
from sqlalchemy.ext.asyncio import AsyncSession
from services.tg.spam.update_spam_message import update_spam_message


async def delete_all_messages_with_vacancy_from_users_and_update_message(
    callback: CallbackQuery,
    callback_data: NotSpamButDeleteMessagesForSpamVacancyCallback,
    session: AsyncSession,
):
    await delete_all_messages_with_vacancy_from_users(callback_data, session)

    await update_spam_message(
        callback,
        "spam/update_spam_message_delete_all_spam_messages"
    )