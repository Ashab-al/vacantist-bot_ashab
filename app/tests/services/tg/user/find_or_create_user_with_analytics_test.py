from unittest.mock import AsyncMock, patch

import pytest
from aiogram.types import User as AiogramTgUser
from models.user import User
from services.tg.user.find_or_create_user_with_analytics import (
    find_or_create_user_with_analytics,
)
from tests.factories.user import UserFactoryWithoutSubscriptions


@pytest.mark.asyncio
@patch("services.tg.user.find_or_create_user_with_analytics.send_analytics")
@patch("services.tg.user.find_or_create_user_with_analytics.find_user_by_platform_id")
async def test_find_or_create_user_with_analytics(
    mock_find_user_by_platform_id, mock_send_analytics
):
    """Проверяет создание нового пользователя когда пользователь существует."""
    new_user: User = UserFactoryWithoutSubscriptions()
    is_bot = False
    mock_find_user_by_platform_id.return_value = new_user
    mock_db = AsyncMock()

    from_user: AiogramTgUser = AiogramTgUser(
        id=new_user.platform_id, is_bot=is_bot, first_name=new_user.first_name
    )

    result: User = await find_or_create_user_with_analytics(mock_db, from_user)

    mock_find_user_by_platform_id.assert_awaited_once_with(mock_db, from_user.id)
    mock_send_analytics.assert_not_awaited()
    assert isinstance(result, User)
    assert result.platform_id == new_user.platform_id


@pytest.mark.asyncio
@patch("services.tg.user.find_or_create_user_with_analytics.create_user")
@patch("services.tg.user.find_or_create_user_with_analytics.send_analytics")
@patch("services.tg.user.find_user_by_platform_id.get_user_by_platform_id")
async def test_find_or_create_user_with_analytics_when_user_is_not_exist(
    mock_get_user_by_platform_id, mock_send_analytics, mock_create_user
):
    """Проверяет создание нового пользователя когда пользователь не существует."""
    new_user: User = UserFactoryWithoutSubscriptions()

    mock_get_user_by_platform_id.return_value = None
    mock_create_user.return_value = new_user

    is_bot = False
    mock_db = AsyncMock()

    from_user: AiogramTgUser = AiogramTgUser(
        id=new_user.platform_id, is_bot=is_bot, first_name=new_user.first_name
    )

    result: User = await find_or_create_user_with_analytics(mock_db, from_user)
    mock_get_user_by_platform_id.assert_awaited_once_with(
        mock_db, from_user.id
    )
    mock_create_user.assert_awaited_once_with(mock_db, from_user)
    mock_send_analytics.assert_awaited_once_with(mock_db, new_user)
    assert isinstance(result, User)
    assert result.platform_id == new_user.platform_id