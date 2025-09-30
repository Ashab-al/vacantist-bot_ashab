from aiogram import Router, F
from aiogram.types import ChatMemberUpdated
from aiogram.filters.chat_member_updated import ChatMemberUpdatedFilter, MEMBER, KICKED
from sqlalchemy.ext.asyncio import AsyncSession
from database import with_session
from services.tg.user.current_user import current_user
from services.tg.user.status_changes_for_block import status_changes_for_block

router = Router(name="Обработчик блокировки и разблокировки бота")
router.my_chat_member.filter(F.chat.type == "private")

@router.my_chat_member(ChatMemberUpdatedFilter(member_status_changed=KICKED))
@with_session
async def user_blocked_bot(
    event: ChatMemberUpdated,
    session: AsyncSession
):
    await status_changes_for_block(session, event.from_user)

@router.my_chat_member(ChatMemberUpdatedFilter(member_status_changed=MEMBER))
@with_session
async def user_unblocked_bot(
    event: ChatMemberUpdated,
    session: AsyncSession
):
    await current_user(session, event=event)
