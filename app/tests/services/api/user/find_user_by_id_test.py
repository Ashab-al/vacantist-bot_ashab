import random
from unittest.mock import AsyncMock, patch

import pytest
from exceptions.user_not_found_error import UserNotFoundError
from models.user import User
from schemas.api.users.show.request import ShowUserRequest
from services.api.user.find_user_by_id import find_user_by_id
from tests.factories.user import UserFactoryWithoutSubscriptions


@pytest.mark.asyncio
@patch("services.api.user.find_user_by_id.get_user_by_id")
async def test_find_user_by_id(mock_get_user_by_id):
    """Проверяет поиск пользователя по id"""
    mock_db = AsyncMock()
    new_user: User = UserFactoryWithoutSubscriptions()
    mock_get_user_by_id.return_value = new_user
    user: User = await find_user_by_id(mock_db, ShowUserRequest(id=new_user.id))

    mock_get_user_by_id.assert_awaited_once_with(mock_db, new_user.id)
    assert isinstance(user, User)
    assert user.id == new_user.id
    assert user.platform_id == new_user.platform_id
    assert user.first_name == new_user.first_name


@pytest.mark.asyncio
@patch("services.api.user.find_user_by_id.get_user_by_id")
async def test_find_user_by_id_when_user_not_exist(mock_get_user_by_id):
    """Проверяет поиск не существующего пользователя по id"""
    mock_db = AsyncMock()
    user_id: int = random.randint(1, 100)
    mock_get_user_by_id.return_value = None
    with pytest.raises(UserNotFoundError):
        await find_user_by_id(mock_db, ShowUserRequest(id=user_id))

    mock_get_user_by_id.assert_awaited_once_with(mock_db, user_id)
