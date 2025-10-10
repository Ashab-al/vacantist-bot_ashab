"""
Модуль для инициализации и управления жизненным циклом Telegram-бота.

Этот файл содержит создание экземпляров бота и диспетчера, а также функции
для отправки уведомлений администратору при запуске и остановке бота.

Attributes:
    bot (Bot): Экземпляр Telegram-бота с предустановленными свойствами.
    dp (Dispatcher): Диспетчер для регистрации хэндлеров и обработки событий.

Functions:
    start_bot(): Отправить администратору уведомление о запуске бота.
    stop_bot(): Отправить администратору уведомление об остановке бота.
"""

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from config import settings


bot = Bot(
    token=settings.bot_token, default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
"""Экземпляр Telegram-бота с предустановленными свойствами."""

dp = Dispatcher()
"""Диспетчер для регистрации хэндлеров и обработки событий."""


async def start_bot():
    """
    Отправить администратору уведомление о запуске бота.

    При успешном старте бот отправляет сообщение с текстом «Я запущен🥳».
    В случае ошибки при отправке сообщение игнорируется.
    """
    try:
        await bot.send_message(settings.admin_id, f"Я запущен🥳.")
    except:
        pass


async def stop_bot():
    """
    Отправить администратору уведомление об остановке бота.

    При завершении работы бот отправляет сообщение с текстом «Бот остановлен.».
    В случае ошибки при отправке сообщение игнорируется.
    """
    try:
        await bot.send_message(settings.admin_id, "Бот остановлен.")
    except:
        pass
