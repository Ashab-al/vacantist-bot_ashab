from unittest.mock import AsyncMock, patch

import pytest
from aiogram.types import User as AiogramTgUser
from models.user import User
from services.tg.user.create_user import create_user
from tests.factories.user import UserFactoryWithoutSubscriptions


@pytest.mark.asyncio
@patch("services.tg.user.create_user.get_user_by_platform_id")
async def test_create_user(mock_get_user_by_platform_id):
    """Проверяет создание нового пользователя"""
    mock_get_user_by_platform_id.return_value = None
    mock_db = AsyncMock()
    is_bot: bool = False
    new_user: User = UserFactoryWithoutSubscriptions()
    new_user.bonus = User.DEFAULT_BONUS
    aiogram_user: AiogramTgUser = AiogramTgUser(
        id=new_user.platform_id,
        is_bot=is_bot,
        first_name=new_user.first_name,
        username=new_user.username
    )

    result = await create_user(mock_db, aiogram_user)

    mock_get_user_by_platform_id.assert_awaited_once_with(mock_db, new_user.platform_id)
    assert result.platform_id == new_user.platform_id
    assert result.first_name == new_user.first_name
    assert result.username == new_user.username
    assert result.point == new_user.point
    assert result.bonus == new_user.bonus
    assert result.bot_status == new_user.bot_status
