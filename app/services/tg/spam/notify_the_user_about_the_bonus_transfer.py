from aiogram import Bot
from models import User
from lib.tg.common import jinja_render


async def notify_the_user_about_the_bonus_transfer(
    user: User,
    bot: Bot,
):
    await bot.send_message(
        chat_id=user.platform_id,
        text=await jinja_render(
            "spam/notify_the_user_about_the_bonus_transfer",
            {"user": user}
        )
    )
