from aiogram import Bot, F, Router
from aiogram.enums.chat_type import ChatType
from aiogram.types import CallbackQuery
from bot.filters.callback.spam_vacancy_callback import (
    IncrementUserBonusForSpamVacancyCallback,
    NotSpamButDeleteMessagesForSpamVacancyCallback,
    RejectSpamVacancyCallback,
    SpamAndIncrementUserBonusForSpamVacancyCallback,
    SpamVacancyCallback,
    SpamVacancyCallbackForAdmin,
)
from config import settings
from database import with_session
from services.tg.spam.add_to_spam_and_increment_user_bonus_then_update_message import (
    add_to_spam_and_increment_user_bonus_then_update_message,
)
from services.tg.spam.delete_all_messages_and_confirm_add_vacancy_to_blacklist import (
    delete_all_messages_and_confirm_add_vacancy_to_blacklist,
)
from services.tg.spam.delete_all_messages_with_vacancy_from_users import (
    delete_all_messages_with_vacancy_from_users,
)
from services.tg.spam.delete_all_messages_with_vacancy_from_users_and_update_message import (
    delete_all_messages_with_vacancy_from_users_and_update_message,
)
from services.tg.spam.increment_bonus_and_notify_user_then_update_message import (
    increment_bonus_and_notify_user_then_update_message,
)
from services.tg.vacancy.send_spam_vacancy_in_admin_group import (
    send_spam_vacancy_in_admin_group,
)
from sqlalchemy.ext.asyncio import AsyncSession

router = Router(name="Обработчик логики связанной со спамом")
router.message.filter((F.chat.id == settings.admin_chat_id))


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
    - Вызывает сервис `send_spam_vacancy_in_admin_group` для обработки жалобы
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


@router.callback_query(SpamVacancyCallbackForAdmin.filter())
@with_session
async def spam_vacancy_for_admin(
    callback: CallbackQuery,
    callback_data: SpamVacancyCallbackForAdmin,
    session: AsyncSession,
):
    """Нажатие на кнопку 'Подтвердить спам'"""
    await callback.answer()
    await delete_all_messages_and_confirm_add_vacancy_to_blacklist(
        callback, callback_data, session
    )


@router.callback_query(IncrementUserBonusForSpamVacancyCallback.filter())
@with_session
async def increment_user_bonus_for_spam_vacancy(
    callback: CallbackQuery,
    callback_data: IncrementUserBonusForSpamVacancyCallback,
    session: AsyncSession,
    bot: Bot,
):
    """
    Нажатие на кнопку 'Зачислить 1 бонус клиенту'
    """
    await callback.answer()
    await increment_bonus_and_notify_user_then_update_message(
        callback, callback_data, session, bot
    )


@router.callback_query(SpamAndIncrementUserBonusForSpamVacancyCallback.filter())
async def spam_and_increment_user_bonus_for_spam_vacancy(
    callback: CallbackQuery,
    callback_data: SpamAndIncrementUserBonusForSpamVacancyCallback,
    bot: Bot,
):
    await callback.answer()
    await add_to_spam_and_increment_user_bonus_then_update_message(
        callback, callback_data, bot
    )


@router.callback_query(NotSpamButDeleteMessagesForSpamVacancyCallback.filter())
@with_session
async def not_spam_but_delete_messages_for_spam_vacancy(
    callback: CallbackQuery,
    callback_data: NotSpamButDeleteMessagesForSpamVacancyCallback,
    session: AsyncSession,
):
    await callback.answer()
    await delete_all_messages_with_vacancy_from_users_and_update_message(
        callback, callback_data, session
    )
