import random
from unittest.mock import patch

import pytest
from fastapi import status
from models.user import User
from tests.factories.user import UserFactoryWithoutSubscriptions


@pytest.mark.asyncio
@patch("api.users.list.ListUsersResponse")
@patch("services.api.user.users_list.get_all_users")
async def test_list_users(mock_get_all_users, mock_list_users_response, client):
    """Тестирует эндпоинт возврата списка всех существующих пользователей"""
    users_count: int = random.randint(4, 10)

    users: list[User] = [UserFactoryWithoutSubscriptions() for _ in range(users_count)]
    mock_get_all_users.return_value = users
    mock_list_users_response.return_value = {"users": users}
    response = await client.get("/users/")

    assert response.status_code == status.HTTP_200_OK
    assert len(response.json().get("users")) == len(users)
