import asyncio
import logging
import random
from asyncio import TaskGroup

from aiogram import Bot
from aiogram.exceptions import TelegramForbiddenError
from bot.create_bot import bot
from bot.keyboards.vacancy_keyboard import vacancy_keyboard
from config import settings
from database import get_async_session_for_bot
from enums.bot_status_enum import BotStatusEnum
from lib.tg.common import jinja_render
from models.sent_message import SentMessage
from models.user import User
from models.vacancy import Vacancy
from query_objects.users.find_users_where_have_subscribe_to_category import (
    find_users_where_have_subscribe_to_category,
)
from query_objects.users.get_user_by_id import get_user_by_id
from query_objects.vacancies.find_vacancy_by_id import find_vacancy_by_id
from services.tg.admin_alert import (
    admin_alert_mailing_errors,
    admin_alert_mailing_vacancies,
)
from services.tg.user.update_bot_status import update_bot_status
from sqlalchemy.ext.asyncio import AsyncSession


async def sender_vacancy(vacancy_id: int) -> None:
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
    await admin_alert_mailing_vacancies(
        bot, f"Запущена рассылка вакансии с ID: {vacancy_id}"
    )

    logging.info("Запущена рассылка вакансии с ID: %s", vacancy_id)

    async with get_async_session_for_bot() as db:
        vacancy: Vacancy | None = await find_vacancy_by_id(db, vacancy_id)

        if vacancy is None:
            await admin_alert_mailing_errors(
                bot, f"Вакансия с ID {vacancy_id} не найдена"
            )
            raise ValueError("Vacancy not found")

        users: list[User] = await find_users_where_have_subscribe_to_category(
            db, vacancy.category_id
        )
        if not users:
            await admin_alert_mailing_errors(
                bot, f"Для вакансии '{vacancy.title}' не найдено подписчиков."
            )
            raise ValueError("No subscribed users found")

        await admin_alert_mailing_vacancies(
            bot,
            f"Рассылка вакансии '{vacancy.title}' для {len(users)} пользователей.",
        )
        # Отправка вакансии всем подписанным пользователям.
        tasks = [
            asyncio.create_task(send_vacancy_to_user(bot, user, vacancy, db))
            for user in users
        ]
        await asyncio.gather(
            *tasks
        )  # сделать так чтобы возвращались объекты SentMessage
        await db.commit()

    logging.info("Рассылка вакансии с ID: %s завершена", vacancy_id)
    await admin_alert_mailing_vacancies(
        bot, f"Рассылка вакансии с ID: {vacancy_id} завершена."
    )


async def send_vacancy_to_user(
    bot: Bot, user: User, vacancy: Vacancy, db: AsyncSession
) -> None:
    """Отправить вакансию пользователю с задержкой."""
    await asyncio.sleep(
        random.randint(settings.min_delay_seconds, settings.max_delay_seconds)
    )
    try:
        result = await bot.send_message(
            chat_id=user.platform_id,
            text=await jinja_render("vacancy", {"vacancy": vacancy, "user": user}),
            reply_markup=await vacancy_keyboard(vacancy=vacancy, user=user),
        )
        db.add(
            SentMessage(
                user_id=user.id,
                vacancy_id=vacancy.id,
                message_id=result.message_id,
            )
        )
        logging.info(str(result))
    except TelegramForbiddenError as e:
        logging.error(str(e))
        await admin_alert_mailing_errors(
            bot, str(e) + "\n\nTelegramForbiddenError sender_worker"
        )
        async with get_async_session_for_bot() as session:
            await update_bot_status(
                db=session,
                user=await get_user_by_id(session, user.id),
                new_status=BotStatusEnum.BOT_BLOCKED,
            )

    except Exception as e:  # pylint: disable=broad-exception-caught
        logging.error(str(e))
        await admin_alert_mailing_errors(bot, str(e) + "\n\nsender_worker")
