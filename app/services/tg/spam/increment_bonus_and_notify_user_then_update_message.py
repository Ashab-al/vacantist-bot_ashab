from aiogram import Bot
from aiogram.types import CallbackQuery
from bot.filters.callback.spam_vacancy_callback import (
    IncrementUserBonusForSpamVacancyCallback,
)
from models import User
from services.tg.spam.increment_user_bonus import increment_bonus_and_notify_user
from services.tg.spam.update_spam_message import update_spam_message
from sqlalchemy.ext.asyncio import AsyncSession


async def increment_bonus_and_notify_user_then_update_message(
    callback: CallbackQuery,
    callback_data: IncrementUserBonusForSpamVacancyCallback,
    session: AsyncSession,
    bot: Bot,
) -> None:
    user: User = await increment_bonus_and_notify_user(callback_data, session, bot)
    await update_spam_message(callback, "spam/increment_user_bonus", {"user": user})
