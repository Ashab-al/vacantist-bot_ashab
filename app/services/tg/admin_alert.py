from aiogram import Bot
from config import settings


async def admin_alert(bot: Bot, text: str) -> None:
    """
    Отправить в группу админа уведомление

    Args:
        bot (Bot): Экземпляр бота, для отправки сообщения
        text (str): Текст, который нужно отправить в группу
    """
    await bot.send_message(chat_id=settings.admin_chat_id, text=text)
