from aiogram import Bot
from config import settings


async def admin_alert_mailing_vacancies(bot: Bot, text: str) -> None:
    """
    Отправить в группу админа уведомление

    Args:
        bot (Bot): Экземпляр бота, для отправки сообщения
        text (str): Текст, который нужно отправить в группу
    """
    await bot.send_message(
        chat_id=settings.admin_chat_id,
        text=text,
        message_thread_id=settings.mailing_vacancies_thread_id
    )

async def admin_alert_mailing_errors(bot: Bot, text: str) -> None:
    """
    Отправить в группу админа уведомление

    Args:
        bot (Bot): Экземпляр бота, для отправки сообщения
        text (str): Текст, который нужно отправить в группу
    """
    await bot.send_message(
        chat_id=settings.admin_chat_id,
        text=text,
        message_thread_id=settings.mailing_errors_thread_id
    )

async def admin_alert_mailing_payments_info(bot: Bot, text: str) -> None:
    """
    Отправить в группу админа уведомление

    Args:
        bot (Bot): Экземпляр бота, для отправки сообщения
        text (str): Текст, который нужно отправить в группу
    """
    await bot.send_message(
        chat_id=settings.admin_chat_id,
        text=text,
        message_thread_id=settings.mailing_payments_thread_id
    )

async def admin_alert_mailing_new_users(bot: Bot, text: str) -> None:
    """
    Отправить в группу админа уведомление

    Args:
        bot (Bot): Экземпляр бота, для отправки сообщения
        text (str): Текст, который нужно отправить в группу
    """
    await bot.send_message(
        chat_id=settings.admin_chat_id,
        text=text,
        message_thread_id=settings.mailing_new_users_thread_id
    )
