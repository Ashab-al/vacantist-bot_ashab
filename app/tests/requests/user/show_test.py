import random
from unittest.mock import patch

import pytest
from fastapi import status
from models.user import User
from tests.factories.user import UserFactoryWithoutSubscriptions


@pytest.mark.asyncio
@patch("services.api.user.find_user_by_id.get_user_by_id")
async def test_show(mock_get_user_by_id, client):
    """Тестирует эндпоинт который возвращает данные о пользователе"""
    user: User = UserFactoryWithoutSubscriptions()
    mock_get_user_by_id.return_value = user
    response = await client.get(f"/users/{user.id}")

    assert response.status_code == status.HTTP_200_OK
    assert response.json().get("id") == user.id


@pytest.mark.asyncio
@patch("services.api.user.find_user_by_id.get_user_by_id")
async def test_show_when_user_is_not_exist(mock_get_user_by_id, client):
    """Тестирует эндпоинт который вовзращает ошибку, если пользователь не существует"""
    user_id: int = random.randint(1, 100)
    mock_get_user_by_id.return_value = None
    response = await client.get(f"/users/{user_id}")

    assert response.status_code == status.HTTP_404_NOT_FOUND
