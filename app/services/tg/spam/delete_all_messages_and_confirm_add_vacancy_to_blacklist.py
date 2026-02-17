from aiogram.types import CallbackQuery
from bot.filters.callback.spam_vacancy_callback import SpamVacancyCallbackForAdmin
from services.tg.spam.admin_confirm_add_vacancy_to_blacklist_then_update_message import (
    admin_confirm_add_vacancy_to_blacklist_then_update_message,
)
from services.tg.spam.delete_all_messages_with_vacancy_from_users import (
    delete_all_messages_with_vacancy_from_users,
)
from sqlalchemy.ext.asyncio import AsyncSession


async def delete_all_messages_and_confirm_add_vacancy_to_blacklist(
    callback: CallbackQuery,
    callback_data: SpamVacancyCallbackForAdmin,
    session: AsyncSession,
):
    await delete_all_messages_with_vacancy_from_users(callback_data, session)
    await admin_confirm_add_vacancy_to_blacklist_then_update_message(
        callback, callback_data, session
    )
