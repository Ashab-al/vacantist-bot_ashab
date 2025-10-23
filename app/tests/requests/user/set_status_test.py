import random
from unittest.mock import patch

import pytest
from enums.bot_status_enum import BotStatusEnum
from fastapi import status
from models.user import User
from tests.factories.user import UserFactoryWithoutSubscriptions


@pytest.mark.asyncio
@patch("services.api.user.find_user_by_id.get_user_by_id")
async def test_set_status(mock_get_user_by_id, client):
    """Тестирует эндпоинт обновления статуса у пользователя"""
    user: User = UserFactoryWithoutSubscriptions()
    mock_get_user_by_id.return_value = user
    response = await client.post(
        f"/users/{user.id}/set_status",
        json={"bot_status": BotStatusEnum.BOT_BLOCKED.value},
    )

    assert response.status_code == status.HTTP_200_OK


@pytest.mark.asyncio
@patch("services.api.user.find_user_by_id.get_user_by_id")
async def test_set_status_when_user_is_not_exist(mock_get_user_by_id, client):
    """Тестирует эндпоинт обновления статуса у пользователя, которого не существует"""
    user_id: int = random.randint(1, 100)
    mock_get_user_by_id.return_value = None
    response = await client.post(
        f"/users/{user_id}/set_status",
        json={"bot_status": BotStatusEnum.BOT_BLOCKED.value},
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND
