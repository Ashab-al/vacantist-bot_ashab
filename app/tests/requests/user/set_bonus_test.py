import random
from unittest.mock import patch

import pytest
from fastapi import status
from models.user import User
from tests.factories.user import UserFactoryWithoutSubscriptions


@pytest.mark.asyncio
@patch("services.api.user.find_user_by_id.get_user_by_id")
async def test_set_bonus(mock_get_user_by_id, client):
    """Тестирует эндпоинт обновления количество бонусов у пользователя"""
    bonus_count: int = random.randint(1, 100)
    user: User = UserFactoryWithoutSubscriptions()
    mock_get_user_by_id.return_value = user
    response = await client.post(
        f"/users/{user.id}/set_bonus", json={"count": bonus_count}
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json().get("bonus") == bonus_count


@pytest.mark.asyncio
@patch("services.api.user.find_user_by_id.get_user_by_id")
async def test_set_bonus_when_user_is_not_exist(mock_get_user_by_id, client):
    """Тестирует эндпоинт обновления количество бонусов у пользователя, которого не существует"""
    bonus_count: int = random.randint(1, 100)
    user_id: int = random.randint(1, 100)
    mock_get_user_by_id.return_value = None
    response = await client.post(
        f"/users/{user_id}/set_bonus", json={"count": bonus_count}
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND
