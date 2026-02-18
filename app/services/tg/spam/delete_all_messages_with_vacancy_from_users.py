import asyncio
import logging
from asyncio import TaskGroup
from random import randint

from bot.create_bot import bot
from bot.filters.callback.spam_vacancy_callback import SpamVacancyCallbackForAdmin
from config import settings
from models import SentMessage
from query_objects.sent_message.find_sent_messages_by_vacancy_id import (
    find_sent_messages_by_vacancy_id,
)
from sqlalchemy.ext.asyncio import AsyncSession


async def delete_all_messages_with_vacancy_from_users(
    callback_data: SpamVacancyCallbackForAdmin,
    session: AsyncSession
):
    """
    Удаляет все сообщения с указанной вакансией из чатов пользователей и очищает записи из базы данных.

    Находит все отправленные сообщения по ID вакансии. Если сообщения не найдены — выбрасывает ValueError.
    Для каждого сообщения асинхронно удаляет его в Telegram и удаляет запись из БД.
    В конце фиксирует изменения в сессии.

    :param callback_data: Данные коллбэка, содержащие ID вакансии.
    :param session: Асинхронная сессия SQLAlchemy для работы с базой данных.
    :raises ValueError: Если сообщения с указанной вакансией не найдены.
    """
    sent_messages: list[tuple[SentMessage, int]] | None = (
        await find_sent_messages_by_vacancy_id(callback_data.vacancy_id, session)
    )

    if sent_messages is None:
        raise ValueError("Сообщения не найдены")
    await _delete_all_messages(sent_messages, session)
    await session.commit()
    logging.info("Удаление сообщений завершено и удалены данные из базы")


async def _delete_all_messages(
    sent_messages: list[tuple[SentMessage, int]], session: AsyncSession
):
    """
    Асинхронно удаляет все указанные сообщения параллельно с использованием TaskGroup.

    Обрабатывает список кортежей (сообщение, chat_id), создавая задачу на удаление для каждого.
    После завершения всех задач логирует успешное удаление.

    :param sent_messages: Список кортежей, каждый содержит объект SentMessage и chat_id пользователя.
    :param session: Асинхронная сессия SQLAlchemy для удаления записей из БД.
    """
    async with TaskGroup() as tg:
        for sent_message, chat_id in sent_messages:
            tg.create_task(_delete_message(sent_message, chat_id, session))
    logging.info("Все сообщения удалены")


async def _delete_message(
    sent_message: SentMessage, chat_id: int, session: AsyncSession
):
    """
    Удаляет одно сообщение у пользователя через Telegram Bot API.

    Перед удалением выполняется случайная задержка (чтобы не перегружать запросами).
    После попытки удаления удаляет запись из базы данных. Ошибки перехватываются и логируются.

    :param sent_message: Объект SentMessage, представляющий сообщение в БД.
    :param chat_id: ID чата пользователя, где нужно удалить сообщение.
    :param session: Асинхронная сессия SQLAlchemy для удаления записи из БД.
    """
    try:
        logging.info(
            "Удаление сообщения у %s, id сообщения: %s",
            chat_id,
            sent_message.message_id,
        )
        await asyncio.sleep(
            randint(settings.min_delay_seconds, settings.max_delay_seconds)
        )
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
    except Exception as e:
        logging.error(e)
        return
