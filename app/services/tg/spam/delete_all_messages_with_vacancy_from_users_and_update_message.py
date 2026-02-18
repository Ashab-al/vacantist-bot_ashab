from aiogram.types import CallbackQuery
from bot.filters.callback.spam_vacancy_callback import (
    NotSpamButDeleteMessagesForSpamVacancyCallback,
)
from services.tg.spam.delete_all_messages_with_vacancy_from_users import (
    delete_all_messages_with_vacancy_from_users,
)
from services.tg.spam.update_spam_message import update_spam_message
from sqlalchemy.ext.asyncio import AsyncSession


async def delete_all_messages_with_vacancy_from_users_and_update_message(
    callback: CallbackQuery,
    callback_data: NotSpamButDeleteMessagesForSpamVacancyCallback,
    session: AsyncSession,
):
    """
    Удаляет все сообщения с указанной вакансией у пользователей и обновляет сообщение в админ-группе.

    Используется, когда вакансия признана не спамом, но ранее была разослана пользователям —
    требуется очистка. После удаления сообщений статус в админ-чате обновляется с помощью шаблона.

    :param callback: Объект CallbackQuery, содержащий контекст взаимодействия.
    :param callback_data: Данные коллбэка с ID вакансии, которую нужно обработать.
    :param session: Асинхронная сессия SQLAlchemy для выполнения операций в БД.
    """
    await delete_all_messages_with_vacancy_from_users(callback_data, session)
    await update_spam_message(
        callback, "spam/update_spam_message_delete_all_spam_messages"
    )
