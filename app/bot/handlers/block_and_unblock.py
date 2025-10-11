"""Модуль работы с Telegram-ботом через aiogram."""

from aiogram import F, Router
from aiogram.filters.chat_member_updated import KICKED, MEMBER, ChatMemberUpdatedFilter
from aiogram.types import ChatMemberUpdated
from database import with_session
from services.tg.user.current_user import current_user
from services.tg.user.status_changes_for_block import status_changes_for_block
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
        Производит обновление статуса пользователя в базе данных через `status_changes_for_block`.
    """
    await status_changes_for_block(session, event.from_user)


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
        Производит обновление или создание пользователя в базе данных через `current_user`.
    """
    await current_user(session, event=event)
