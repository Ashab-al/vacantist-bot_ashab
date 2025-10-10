import pytest
from models.user import User
from services.api.user.set_status import set_status
import random
from schemas.api.users.set_status.request import (
    SetStatusUserIdRequest,
    SetStatusRequest,
)
from enums.bot_status_enum import BotStatusEnum


@pytest.mark.asyncio
async def test_set_status(session, new_tg_user: User):
    """Проверяет обновление статуса у пользователя"""

    user: User = await set_status(
        session,
        SetStatusUserIdRequest(id=new_tg_user.id),
        SetStatusRequest(bot_status=BotStatusEnum.BOT_BLOCKED),
    )

    assert isinstance(user, User)
    assert user.bot_status == BotStatusEnum.BOT_BLOCKED
    assert user.id == new_tg_user.id
    assert user.platform_id == new_tg_user.platform_id
    assert user.first_name == new_tg_user.first_name


@pytest.mark.asyncio
async def test_set_status_when_user_not_exist(session):
    """Проверяет обновление статуса у не существующего пользователя"""
    user_id: int = random.randint(1, 100)

    with pytest.raises(ValueError, match=f"Пользователя по id - {user_id} нет в базе"):
        await set_status(
            session,
            SetStatusUserIdRequest(id=user_id),
            SetStatusRequest(bot_status=BotStatusEnum.BOT_BLOCKED),
        )
