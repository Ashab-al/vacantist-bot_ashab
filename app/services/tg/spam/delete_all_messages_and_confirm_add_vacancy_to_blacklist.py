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
    """
    Удаляет все сообщения с указанной вакансией у пользователей,
    затем подтверждает добавление вакансии в чёрный список и обновляет сообщение в админ-группе.

    Эта функция объединяет два действия:
    1. Массовое удаление сообщений с вакансией через сервис `delete_all_messages_with_vacancy_from_users`.
    2. Подтверждение спама и обновление статуса сообщения в админ-чате через
       `admin_confirm_add_vacancy_to_blacklist_then_update_message`.

    :param callback: Объект CallbackQuery от Telegram, содержит контекст нажатия кнопки.
    :param callback_data: Данные коллбэка с информацией о вакансии (например, её ID).
    :param session: Асинхронная сессия SQLAlchemy для работы с базой данных.
    """
    await delete_all_messages_with_vacancy_from_users(callback_data, session)
    await admin_confirm_add_vacancy_to_blacklist_then_update_message(
        callback, callback_data, session
    )
