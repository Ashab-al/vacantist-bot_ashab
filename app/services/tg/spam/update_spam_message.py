from sqlalchemy.ext.asyncio import AsyncSession

from services.tg.spam.add_vacancy_to_blacklist import add_vacancy_to_blacklist
from aiogram import Bot
from aiogram.types import CallbackQuery
from bot.filters.callback.spam_vacancy_callback import (
    SpamVacancyCallbackForAdmin,
)
from lib.tg.common import jinja_render

async def update_spam_message(
    callback: CallbackQuery,
    action: str,
    context: dict | None = None,
) -> None:
    await callback.message.edit_text(
        text=await jinja_render(
            action,
            {
                "text":callback.message.text,
                **(context or {})
            }
        ),
        reply_markup=callback.message.reply_markup
    )
