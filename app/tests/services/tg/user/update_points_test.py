import random
from unittest.mock import AsyncMock

import pytest
from aiogram.types import User as AiogramTgUser
from exceptions.user_not_found_error import UserNotFoundError
from models.user import User
from services.tg.user.update_points import update_points
from tests.factories.user import UserFactoryWithoutSubscriptions


@pytest.mark.asyncio
async def test_update_points(mocker):
    """Проверяет обновление количества поинтов"""
    count_points: int = random.randint(3, 100)
    is_bot: bool = False
    new_user: User = UserFactoryWithoutSubscriptions()
    aiogram_user: AiogramTgUser = AiogramTgUser(
        id=new_user.platform_id, is_bot=is_bot, first_name=new_user.first_name
    )

    mock_get_user_by_platform_id = mocker.patch(
        "services.tg.user.find_user_by_platform_id.get_user_by_platform_id",
        return_value=new_user,
    )
    mock_db = AsyncMock()
    user: User = await update_points(mock_db, aiogram_user, count_points)

    mock_get_user_by_platform_id.assert_awaited_once_with(mock_db, aiogram_user.id)
    mock_db.commit.assert_awaited_once()
    mock_db.refresh.assert_awaited_once_with(user)
    assert user.point == count_points


@pytest.mark.asyncio
async def test_update_points_when_user_is_not_exist(mocker):
    """Проверяет обновление количества поинтов у несуществующего пользователя"""
    user_id = random.randint(1, 1000)
    is_bot = False
    first_name = "Тестовый"
    username = "test_user"
    count_points: int = random.randint(3, 100)
    aiogram_user = AiogramTgUser(
        id=user_id, is_bot=is_bot, first_name=first_name, username=username
    )
    mock_get_user_by_platform_id = mocker.patch(
        "services.tg.user.find_user_by_platform_id.get_user_by_platform_id",
        return_value=None,
    )
    mock_db = AsyncMock()
    with pytest.raises(UserNotFoundError):
        await update_points(mock_db, aiogram_user, count_points)
    mock_get_user_by_platform_id.assert_awaited_once_with(mock_db, aiogram_user.id)
