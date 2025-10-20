import random
from unittest.mock import AsyncMock, patch

import pytest
from exceptions.user_not_found_error import UserNotFoundError
from models.user import User
from services.tg.user.find_user_by_platform_id import find_user_by_platform_id
from tests.factories.user import UserFactoryWithoutSubscriptions


@pytest.mark.asyncio
@patch("services.tg.user.find_user_by_platform_id.get_user_by_platform_id")
async def test_find_user_by_platform_id(mock_get_user_by_platform_id):
    """Поиск пользователя по platform_id когда пользователь существует."""
    new_user: User = UserFactoryWithoutSubscriptions()

    mock_get_user_by_platform_id.return_value = new_user
    mock_db = AsyncMock()

    result = await find_user_by_platform_id(mock_db, new_user.platform_id)
    mock_get_user_by_platform_id.assert_awaited_once_with(mock_db, new_user.platform_id)
    assert result == new_user


@pytest.mark.asyncio
@patch("services.tg.user.find_user_by_platform_id.get_user_by_platform_id")
async def test_find_user_by_platform_id_when_user_is_not_exist(
    mock_get_user_by_platform_id,
):
    """Поиск пользователя по platform_id когда пользователь не существует."""

    mock_get_user_by_platform_id.return_value = None
    mock_db = AsyncMock()
    platform_id = random.randint(1, 10000)
    with pytest.raises(UserNotFoundError):
        await find_user_by_platform_id(mock_db, platform_id)

    mock_get_user_by_platform_id.assert_awaited_once_with(mock_db, platform_id)
