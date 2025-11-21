import asyncio
import random

from aiogram import Bot
from aiogram.exceptions import TelegramForbiddenError
from bot.keyboards.vacancy_keyboard import vacancy_keyboard
from database import get_async_session_for_bot
from enums.bot_status_enum import BotStatusEnum
from lib.tg.common import jinja_render
from models.user import User
from models.vacancy import Vacancy
from query_objects.users.find_users_where_have_subscribe_to_category import (
    find_users_where_have_subscribe_to_category,
)
from query_objects.users.get_user_by_id import get_user_by_id
from services.tg.admin_alert import admin_alert
from services.tg.user.update_bot_status import update_bot_status

MIN_DELAY = 2
MAX_DELAY = 60


async def sender_worker(queue: asyncio.Queue, bot: Bot) -> None:
    """
    Асинхронный воркер для рассылки вакансий подписанным пользователям.

    Работает в бесконечном цикле: получает вакансии из очереди и рассылает их
    пользователям, подписанным на соответствующую категорию. Между отправками
    сообщений делается пауза в `DELAY` секунд. Завершается при получении `None`
    из очереди.

    Args:
        queue (asyncio.Queue): Асинхронная очередь FIFO, в которую добавляются
            объекты `Vacancy` или `None` для остановки воркера.
        bot (Bot): Экземпляр Telegram-бота, используемый для отправки сообщений.

    Raises:
        TelegramForbiddenError: Если бот не имеет права отправлять сообщения пользователю.
        Exception: При других неожиданных ошибках.

    Notes:
        - Если пользователь заблокировал бота, его статус обновляется в базе данных
          на `BOT_BLOCKED`.
        - Для остановки воркера в очередь нужно положить `None`.
    """
    await admin_alert(bot, "Воркер для рассылки запущен и ждет вакансии...")
    background_tasks: set = set()
    while True:
        print("ЦИКЛ ЗАПУЩЕН, ОЖИДАЮ ВАКАНСИИ")
        vacancy: Vacancy | None = await queue.get()

        if vacancy is None:
            await admin_alert(
                bot, "Получен сигнал на завершение. Воркер останавливается."
            )
            queue.task_done()
            break

        async with get_async_session_for_bot() as db:
            users: list[User] = await find_users_where_have_subscribe_to_category(
                db, vacancy.category_id
            )
            if not users:
                await admin_alert(
                    bot, f"Для вакансии '{vacancy.title}' не найдено подписчиков."
                )
                queue.task_done()
                continue

            await admin_alert(
                bot,
                f"Рассылка вакансии '{vacancy.title}' для {len(users)} пользователей.",
            )
            # Отправка вакансии всем подписанным пользователям.
            for user in users:
                task = asyncio.create_task(send_vacancy_to_user(bot, user, vacancy))
                background_tasks.add(task)
                task.add_done_callback(background_tasks.discard)

        queue.task_done()

    await admin_alert(bot, "ВЫХОД ИЗ ЦИКЛА")


async def send_vacancy_to_user(bot: Bot, user: User, vacancy: Vacancy) -> None:
    """Отправить вакансию пользователю с задержкой."""
    await asyncio.sleep(random.randint(MIN_DELAY, MAX_DELAY))
    try:
        await bot.send_message(
            chat_id=user.platform_id,
            text=await jinja_render("vacancy", {"vacancy": vacancy, "user": user}),
            reply_markup=await vacancy_keyboard(vacancy=vacancy, user=user),
        )
    except TelegramForbiddenError:
        async with get_async_session_for_bot() as db:
            await update_bot_status(
                db=db,
                user=await get_user_by_id(db, user.id),
                new_status=BotStatusEnum.BOT_BLOCKED,
            )
    except Exception as e:  # pylint: disable=broad-exception-caught
        await admin_alert(bot, str(e) + "\n\nsender_worker")
