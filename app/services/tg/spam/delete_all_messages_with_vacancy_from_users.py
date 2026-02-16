from random import randint
import asyncio
from asyncio import TaskGroup
from sqlalchemy.ext.asyncio import AsyncSession

from services.tg.spam.add_vacancy_to_blacklist import add_vacancy_to_blacklist
from aiogram.types import CallbackQuery
from bot.filters.callback.spam_vacancy_callback import (
    SpamVacancyCallbackForAdmin,
)
from lib.tg.common import jinja_render
from services.tg.spam.update_spam_message import update_spam_message
from query_objects.sent_message.find_sent_messages_by_vacancy_id import find_sent_messages_by_vacancy_id

from models import SentMessage
from config import settings
from bot.create_bot import bot
import logging

async def delete_all_messages_with_vacancy_from_users(
    callback_data: SpamVacancyCallbackForAdmin,
    session: AsyncSession
):
    sent_messages: list[tuple[SentMessage, int]] | None = await find_sent_messages_by_vacancy_id(
        callback_data.vacancy_id,
        session
    )

    if sent_messages is None:
        raise ValueError("Сообщения не найдены")
    await _delete_all_messages(sent_messages, session)
    await session.commit()
    logging.info("Удаление сообщений завершено и удалены данные из базы")

async def _delete_all_messages(
    sent_messages: list[tuple[SentMessage, int]],
    session: AsyncSession
):
    async with TaskGroup() as tg:
        for sent_message, chat_id in sent_messages:
            tg.create_task(_delete_message(sent_message, chat_id, session))
    logging.info("Все сообщения удалены")

async def _delete_message(sent_message: SentMessage, chat_id: int, session: AsyncSession):
    try:
        logging.info("Удаление сообщения у %s, id сообщения: %s", chat_id, sent_message.message_id)
        await asyncio.sleep(randint(settings.min_delay_seconds, settings.max_delay_seconds))
        res = await bot.delete_message(chat_id=chat_id, message_id=sent_message.message_id)
        logging.info("Сообщение удалено у %s, id сообщения: %s, статус удаления: %s", chat_id, sent_message.message_id, res)
        await session.delete(sent_message)
    except Exception as e:
        logging.error(e)
        return