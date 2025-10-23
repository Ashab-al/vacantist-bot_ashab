"""Модуль работы с Telegram-ботом через aiogram."""

from aiogram import F, Router
from aiogram.filters.chat_member_updated import KICKED, MEMBER, ChatMemberUpdatedFilter
from aiogram.types import ChatMemberUpdated
from database import with_session
from enums.bot_status_enum import BotStatusEnum
from services.tg.user.find_or_create_user_with_analytics import (
    find_or_create_user_with_analytics,
)
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
    await update_bot_status(
        db=session,
        user=await find_or_create_user_with_analytics(session, event.from_user),
        new_status=BotStatusEnum.BOT_BLOCKED,
    )


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
    await update_bot_status(
        db=session,
        user=await find_or_create_user_with_analytics(session, event.from_user),
        new_status=BotStatusEnum.WORKS,
    )
