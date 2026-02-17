from aiogram.types import CallbackQuery
from lib.tg.common import jinja_render


async def update_spam_message(
    callback: CallbackQuery,
    action: str,
    context: dict | None = None,
) -> None:
    await callback.message.edit_text(
        text=await jinja_render(
            action, {"text": callback.message.text, **(context or {})}
        ),
        reply_markup=callback.message.reply_markup,
    )
