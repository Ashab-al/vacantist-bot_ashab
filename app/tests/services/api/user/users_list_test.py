import random
from unittest.mock import AsyncMock, patch

import pytest
from models.user import User
from services.api.user.users_list import users_list
from tests.factories.user import UserFactoryWithoutSubscriptions


@pytest.mark.asyncio
@patch("services.api.user.users_list.get_all_users")
async def test_users_list(mock_get_all_users):
    """Проверяет получение списка пользователей"""
    user_count = random.randint(3, 10)
    mock_db = AsyncMock()
    users: list[User] = [UserFactoryWithoutSubscriptions() for _ in range(user_count)]
    mock_get_all_users.return_value = users
    user_list: list[User] = await users_list(mock_db)

    mock_get_all_users.assert_awaited_once_with(mock_db)
    assert len(user_list) == user_count
    assert all(isinstance(user, User) for user in user_list)
