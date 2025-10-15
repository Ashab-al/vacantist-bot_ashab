"""Модуль работы с Telegram-ботом через aiogram."""

from aiogram import F, Router
from aiogram.filters.chat_member_updated import KICKED, MEMBER, ChatMemberUpdatedFilter
from aiogram.types import ChatMemberUpdated
from database import with_session
from enums.bot_status_enum import BotStatusEnum
from exceptions.user_not_found_error import UserNotFoundError
from models.user import User
from services.tg.send_analytics import send_analytics
from services.tg.user.create_user import create_user
from services.tg.user.find_user_by_platform_id import find_user_by_platform_id
from services.tg.user.update_bot_status import update_bot_status
from sqlalchemy.ext.asyncio import AsyncSession

router = Router(name="Обработчик блокировки и разблокировки бота")
router.my_chat_member.filter(F.chat.type == "private")


@router.my_chat_member(ChatMemberUpdatedFilter(member_status_changed=KICKED))
@with_session
async def user_blocked_bot(event: ChatMemberUpdated, session: AsyncSession):
    """
    Обрабатывает событие блокировки бота пользователем.

    Args:
        event (ChatMemberUpdated): Событие изменения статуса чата пользователя.
        session (AsyncSession): Асинхронная сессия SQLAlchemy для работы с базой данных.

    Notes:
        Вызывается, когда пользователь блокирует бота в личном чате.
        Производит обновление статуса пользователя в базе данных через `update_bot_status`.
    """
    try:
        user: User = await find_user_by_platform_id(session, event.from_user.id)
    except UserNotFoundError:
        user = await create_user(session, event.from_user)
        await send_analytics(session, user)
    await update_bot_status(session, user, BotStatusEnum.BOT_BLOCKED)


@router.my_chat_member(ChatMemberUpdatedFilter(member_status_changed=MEMBER))
@with_session
async def user_unblocked_bot(event: ChatMemberUpdated, session: AsyncSession):
    """
    Обрабатывает событие разблокировки бота пользователем.

    Args:
        event (ChatMemberUpdated): Событие изменения статуса чата пользователя.
        session (AsyncSession): Асинхронная сессия SQLAlchemy для работы с базой данных.

    Notes:
        Вызывается, когда пользователь разблокирует бота в личном чате.
        Производит обновление в базе данных через `update_bot_status`.
    """
    try:
        user: User = await find_user_by_platform_id(session, event.from_user.id)
    except UserNotFoundError:
        user = await create_user(session, event.from_user)
        await send_analytics(session, user)
    if user.bot_status == BotStatusEnum.BOT_BLOCKED:
        await update_bot_status(session, user, BotStatusEnum.WORKS)
