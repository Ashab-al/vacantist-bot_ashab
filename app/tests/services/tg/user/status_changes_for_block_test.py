import pytest
from aiogram.types import User as AiogramTgUser
import random
from models.user import User
from enums.bot_status_enum import BotStatusEnum
from services.tg.user.status_changes_for_block import status_changes_for_block


@pytest.mark.asyncio
async def test_status_changes_for_block(
    session_factory, 
    new_tg_user
):
    """Проверяет изменение статуса пользователя на `BOT_BLOCKED`"""
    is_bot = False
    aiogram_user = AiogramTgUser(
        id=new_tg_user.platform_id,
        is_bot=is_bot,
        first_name=new_tg_user.first_name,
        username=new_tg_user.username
    )
    async with session_factory() as session:
        user: User = await status_changes_for_block(
            session,
            aiogram_user
        )

    assert user.bot_status == BotStatusEnum.BOT_BLOCKED
    assert user.platform_id == new_tg_user.platform_id
    assert user.id == new_tg_user.id

@pytest.mark.asyncio
async def test_status_changes_for_block_when_user_is_not_exist(
    session_factory
):
    """Проверяет изменение статуса не существующего пользователя на `BOT_BLOCKED`"""
    user_id = random.randint(1, 1000)
    is_bot = False
    first_name = "Тестовый"
    username = "test_user"

    aiogram_user = AiogramTgUser(
        id=user_id,
        is_bot=is_bot,
        first_name=first_name,
        username=username
    )
    with pytest.raises(
        ValueError, 
        match=f"Пользователь не найден в базе {aiogram_user}"
    ):
        async with session_factory() as session:
            await status_changes_for_block(
                session,
                aiogram_user
            )

    