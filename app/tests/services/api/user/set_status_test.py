import random
from unittest.mock import AsyncMock, patch

import pytest
from enums.bot_status_enum import BotStatusEnum
from exceptions.user_not_found_error import UserNotFoundError
from models.user import User
from schemas.api.users.set_status.request import (
    SetStatusRequest,
    SetStatusUserIdRequest,
)
from services.api.user.set_status import set_status
from tests.factories.user import UserFactoryWithoutSubscriptions


@pytest.mark.asyncio
@patch("services.api.user.find_user_by_id.get_user_by_id")
async def test_set_status(mock_get_user_by_id):
    """Проверяет обновление статуса у пользователя"""
    new_user = UserFactoryWithoutSubscriptions()
    mock_db = AsyncMock()
    mock_get_user_by_id.return_value = new_user

    user: User = await set_status(
        mock_db,
        SetStatusUserIdRequest(id=new_user.id),
        SetStatusRequest(bot_status=BotStatusEnum.BOT_BLOCKED),
    )

    mock_get_user_by_id.assert_awaited_once_with(mock_db, new_user.id)
    assert isinstance(user, User)
    assert user.bot_status == BotStatusEnum.BOT_BLOCKED
    assert user.id == new_user.id
    assert user.platform_id == new_user.platform_id
    assert user.first_name == new_user.first_name


@pytest.mark.asyncio
@patch("services.api.user.find_user_by_id.get_user_by_id")
async def test_set_status_when_user_not_exist(mock_get_user_by_id):
    """Проверяет обновление статуса у не существующего пользователя"""
    user_id: int = random.randint(1, 100)
    mock_db = AsyncMock()
    mock_get_user_by_id.return_value = None
    with pytest.raises(UserNotFoundError):
        await set_status(
            mock_db,
            SetStatusUserIdRequest(id=user_id),
            SetStatusRequest(bot_status=BotStatusEnum.BOT_BLOCKED),
        )
