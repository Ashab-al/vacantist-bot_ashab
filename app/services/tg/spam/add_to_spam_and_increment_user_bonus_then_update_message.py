from asyncio import TaskGroup

from aiogram import Bot
from aiogram.types import CallbackQuery
from bot.filters.callback.spam_vacancy_callback import (
    SpamAndIncrementUserBonusForSpamVacancyCallback,
)
from lib.tg.common import jinja_render
from models import User
from services.tg.spam.add_vacancy_to_blacklist import add_vacancy_to_blacklist
from services.tg.spam.delete_all_messages_with_vacancy_from_users import (
    delete_all_messages_with_vacancy_from_users,
)
from services.tg.spam.increment_user_bonus import increment_bonus_and_notify_user
from sqlalchemy.ext.asyncio import AsyncSession


async def add_to_spam_and_increment_user_bonus_then_update_message(
    callback: CallbackQuery,
    callback_data: SpamAndIncrementUserBonusForSpamVacancyCallback,
    session: AsyncSession,
    bot: Bot,
) -> None:
    async with TaskGroup() as tg:
        tg.create_task(
            delete_all_messages_with_vacancy_from_users(callback_data, session)
        )
        tg.create_task(_add_vacancy_to_blacklist(callback, callback_data, session))
        user_task = tg.create_task(
            increment_bonus_and_notify_user(callback_data, session, bot)
        )

    await callback.message.edit_text(
        text=await _generate_text(callback, user_task.result()),
        reply_markup=callback.message.reply_markup,
    )


async def _generate_text(callback: CallbackQuery, user: User) -> str:
    text = await jinja_render(
        "spam/increment_user_bonus", {"text": callback.message.text, "user": user}
    )
    text = await jinja_render("spam/update_spam_message_in_admin_group", {"text": text})

    return text


async def _add_vacancy_to_blacklist(
    callback: CallbackQuery,
    callback_data: SpamAndIncrementUserBonusForSpamVacancyCallback,
    session: AsyncSession,
):
    try:
        await add_vacancy_to_blacklist(callback_data.vacancy_id, session)
    except ValueError as e:

        await callback.message.answer(f"Ошибка: {e}")
