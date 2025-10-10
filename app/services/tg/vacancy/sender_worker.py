from aiogram import Bot
from models.user import User
from sqlalchemy import update
from repositories.users.find_users_where_have_subscribe_to_category import (
    find_users_where_have_subscribe_to_category,
)
from models.vacancy import Vacancy
from bot.keyboards.vacancy_keyboard import vacancy_keyboard
from lib.tg.common import jinja_render
from aiogram.exceptions import TelegramForbiddenError
import asyncio
from database import get_async_session_for_bot
from enums.bot_status_enum import BotStatusEnum
from config import settings
from sqlalchemy.ext.asyncio import AsyncSession


DELAY = 0.4


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
    print("Воркер для рассылки запущен и ждет вакансии...")
    await admin_alert(bot, "Воркер для рассылки запущен и ждет вакансии...")
    while True:
        print("ЦИКЛ ЗАПУЩЕН, ОЖИДАЮ ВАКАНСИИ")
        vacancy: Vacancy | None = await queue.get()

        if vacancy is None:
            print("Получен сигнал на завершение. Воркер останавливается.")
            await admin_alert(
                bot, "Получен сигнал на завершение. Воркер останавливается."
            )
            queue.task_done()
            break
        print(f"Начинаю рассылку вакансии: {vacancy.title}")

        async with get_async_session_for_bot() as db:
            users: list[User] = await find_users_where_have_subscribe_to_category(
                db, vacancy.category_id
            )
            blocked_user_ids: list[int] = []
            if not users:
                print(f"Для вакансии '{vacancy.title}' не найдено подписчиков.")
                await admin_alert(
                    bot, f"Для вакансии '{vacancy.title}' не найдено подписчиков."
                )
                queue.task_done()
                continue

            delay: float | int = DELAY

            for user in users:
                try:
                    await bot.send_message(
                        chat_id=user.platform_id,
                        text=await jinja_render(
                            "vacancy", {"vacancy": vacancy, "user": user}
                        ),
                        reply_markup=await vacancy_keyboard(vacancy=vacancy, user=user),
                    )
                except TelegramForbiddenError:
                    blocked_user_ids.append(user.id)
                except Exception as e:
                    await admin_alert(bot, str(e) + "\n" + "\n" + "sender_worker")

                await asyncio.sleep(delay)

            if blocked_user_ids:
                await update_users_bot_status(db, blocked_user_ids)
                await admin_alert(
                    bot,
                    f"Обновлен статус для {len(blocked_user_ids)} заблокированных пользователей.",
                )

        queue.task_done()
        print(f"Рассылка вакансии '{vacancy.title}' завершена.")
        await admin_alert(bot, f"Рассылка вакансии '{vacancy.title}' завершена.")

    print("ВЫХОД ИЗ ЦИКЛА")
    await admin_alert(bot, "ВЫХОД ИЗ ЦИКЛА")


async def update_users_bot_status(
    db: AsyncSession, blocked_user_ids: list[int]
) -> None:
    """
    Обновить `bot_status` на `BOT_BLOCKED` у пользователей

    Args:
        db (AsyncSession): Асинхронная сессия SQLAlchemy для работы с базой данных.
        blocked_user_ids (list[int]): Список id пользователей
    """
    await db.execute(
        (
            update(User)
            .where(User.id.in_(blocked_user_ids))
            .values(bot_status=BotStatusEnum.BOT_BLOCKED)
        )
    )
    await db.commit()


async def admin_alert(bot: Bot, text: str) -> None:
    """
    Отправить в группу админа уведомление

    Args:
        bot (Bot): Экземпляр бота, для отправки сообщения
        text (str): Текст, который нужно отправить в группу
    """
    await bot.send_message(chat_id=settings.admin_chat_id, text=text)
