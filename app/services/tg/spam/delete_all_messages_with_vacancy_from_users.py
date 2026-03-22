import asyncio
import logging
from asyncio import TaskGroup
from random import randint
from aiogram.exceptions import TelegramBadRequest
from bot.create_bot import bot
from bot.filters.callback.spam_vacancy_callback import SpamVacancyCallbackForAdmin
from config import settings
from models import SentMessage
from query_objects.sent_message.find_sent_messages_by_vacancy_id import (
    find_sent_messages_by_vacancy_id,
)
from sqlalchemy.ext.asyncio import AsyncSession
from config import i18n
from lib.tg.common import jinja_render
from database import get_async_session_for_bot


background_tasks: set = set()

async def delete_all_messages_with_vacancy_from_users(
    callback_data: SpamVacancyCallbackForAdmin,
) -> None:
    """
    Удаляет все сообщения с указанной вакансией из чатов пользователей и очищает записи из базы данных.

    Находит все отправленные сообщения по ID вакансии. Если сообщения не найдены — выбрасывает ValueError.
    Для каждого сообщения асинхронно удаляет его в Telegram и удаляет запись из БД.
    В конце фиксирует изменения в сессии.

    :param callback_data: Данные коллбэка, содержащие ID вакансии.
    :param session: Асинхронная сессия SQLAlchemy для работы с базой данных.
    :raises ValueError: Если сообщения с указанной вакансией не найдены.
    """

    task = asyncio.create_task(_find_and_delete_all_messages(callback_data))
    background_tasks.add(task)
    task.add_done_callback(background_tasks.discard)

    return None

async def _find_and_delete_all_messages(
    callback_data: SpamVacancyCallbackForAdmin
):
    """
    Асинхронно удаляет все указанные сообщения параллельно с использованием TaskGroup.

    Обрабатывает список кортежей (сообщение, chat_id), создавая задачу на удаление для каждого.
    После завершения всех задач логирует успешное удаление.

    :param sent_messages: Список кортежей, каждый содержит объект SentMessage и chat_id пользователя.
    :param session: Асинхронная сессия SQLAlchemy для удаления записей из БД.
    """
    seconds = 0.2
    async with get_async_session_for_bot() as session:
        sent_messages: list[tuple[SentMessage, int]] | None = (
            await find_sent_messages_by_vacancy_id(callback_data.vacancy_id, session)
        )
        if sent_messages is None:
            raise ValueError("Сообщения не найдены")

        for sent_message, chat_id in sent_messages:
            await _delete_message(sent_message, chat_id, session)
            await asyncio.sleep(seconds)

        await session.commit()
    logging.info("Все сообщения удалены")


async def _delete_message(
    sent_message: SentMessage,
    chat_id: int,
    session: AsyncSession
):
    """
    Удаляет одно сообщение у пользователя через Telegram Bot API.

    Перед удалением выполняется случайная задержка (чтобы не перегружать запросами).
    После попытки удаления удаляет запись из базы данных. Ошибки перехватываются и логируются.

    :param sent_message: Объект SentMessage, представляющий сообщение в БД.
    :param chat_id: ID чата пользователя, где нужно удалить сообщение.
    :param session: Асинхронная сессия SQLAlchemy для удаления записи из БД.
    """
    logging.info(
        "Удаление сообщения у %s, id сообщения: %s",
        chat_id,
        sent_message.message_id,
    )
    try:
        res = await bot.delete_message(
            chat_id=chat_id, message_id=sent_message.message_id
        )
        logging.info(
            "Сообщение удалено у %s, id сообщения: %s, статус удаления: %s",
            chat_id,
            sent_message.message_id,
            res,
        )
        await session.delete(sent_message)
    except TelegramBadRequest as e:
        logging.error("TelegramBadRequest: %s", e)
        if "message can't be deleted for everyone" in str(e):
            logging.warning("Не удалось удалить сообщение: оно слишком старое или нет прав.")
            logging.warning("Пробуем отредактировать сообщение.")
            await _edit_spam_text(chat_id, sent_message, session)
        else:
            logging.error("Другая ошибка TelegramBadRequest: %s", e)
        return
    except Exception as e:
        logging.error(e)
        return

async def _edit_spam_text(
    chat_id: int,
    sent_message: SentMessage,
    session: AsyncSession
):
    try:
        await bot.edit_message_text(
            chat_id=chat_id,
            message_id=sent_message.message_id,
            text=await jinja_render("spam/this_vacancy_add_to_spam"),
            reply_markup=None
        )
        await session.delete(sent_message)
    except Exception as e:
        logging.error(e)