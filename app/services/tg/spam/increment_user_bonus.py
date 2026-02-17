from aiogram import Bot
from aiogram.types import CallbackQuery
from bot.filters.callback.spam_vacancy_callback import (
    IncrementUserBonusForSpamVacancyCallback,
    SpamAndIncrementUserBonusForSpamVacancyCallback,
)
from models import User
from services.tg.spam.notify_the_user_about_the_bonus_transfer import (
    notify_the_user_about_the_bonus_transfer,
)
from services.tg.user.increment_bonus_by_user_platform_id import (
    increment_bonus_by_user_platform_id,
)
from sqlalchemy.ext.asyncio import AsyncSession


async def increment_bonus_and_notify_user(
    callback_data: (
        IncrementUserBonusForSpamVacancyCallback
        | SpamAndIncrementUserBonusForSpamVacancyCallback
    ),
    session: AsyncSession,
    bot: Bot,
) -> User:
    user: User = await increment_bonus_by_user_platform_id(
        callback_data.user_id, session
    )
    await notify_the_user_about_the_bonus_transfer(user, bot)

    return user
