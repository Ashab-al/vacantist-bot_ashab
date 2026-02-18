from aiogram import Bot
from lib.tg.common import jinja_render
from models import User


async def notify_the_user_about_the_bonus_transfer(
    user: User,
    bot: Bot,
):
    """
    Отправляет пользователю уведомление о начислении бонуса через Telegram-бота.

    Использует шаблон 'spam/notify_the_user_about_the_bonus_transfer' для генерации текста сообщения.
    Сообщение отправляется в личный чат пользователя по его platform_id (Telegram ID).

    :param user: Объект пользователя (User), которому будет отправлено уведомление.
                 Должен содержать атрибут `platform_id` — идентификатор в Telegram.
    :param bot: Экземпляр Aiogram Bot для отправки сообщения.
    """
    await bot.send_message(
        chat_id=user.platform_id,
        text=await jinja_render(
            "spam/notify_the_user_about_the_bonus_transfer", {"user": user}
        ),
    )
