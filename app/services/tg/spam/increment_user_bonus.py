from aiogram.types import CallbackQuery
from aiogram import Bot
from bot.filters.callback.spam_vacancy_callback import (
    IncrementUserBonusForSpamVacancyCallback,
)
from sqlalchemy.ext.asyncio import AsyncSession
from services.tg.user.increment_bonus_by_user_platform_id import increment_bonus_by_user_platform_id
from models import User
from services.tg.spam.update_spam_message import update_spam_message
from services.tg.spam.notify_the_user_about_the_bonus_transfer import notify_the_user_about_the_bonus_transfer


async def increment_user_bonus(
    callback: CallbackQuery,
    callback_data: IncrementUserBonusForSpamVacancyCallback,
    session: AsyncSession,
    bot: Bot
) -> None:
    await callback.answer()

    user: User = await increment_bonus_by_user_platform_id(callback_data.user_id, session)

    await update_spam_message(callback, "spam/increment_user_bonus", {"user": user})

    await notify_the_user_about_the_bonus_transfer(user, bot)
