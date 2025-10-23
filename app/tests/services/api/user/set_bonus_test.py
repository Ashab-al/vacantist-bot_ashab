import random
from unittest.mock import AsyncMock, patch

import pytest
from exceptions.user_not_found_error import UserNotFoundError
from models.user import User
from schemas.api.users.set_bonus.request import SetBonusRequest, SetBonusUserIdRequest
from services.api.user.set_bonus import set_bonus
from tests.factories.user import UserFactoryWithoutSubscriptions


@pytest.mark.asyncio
@patch("services.api.user.find_user_by_id.get_user_by_id")
async def test_set_bonus(mock_get_user_by_id):
    """Проверяет обновление количества бонусов у пользователя"""
    bonus_count = random.randint(10, 100)
    mock_db = AsyncMock()
    new_user = UserFactoryWithoutSubscriptions()
    mock_get_user_by_id.return_value = new_user
    user: User = await set_bonus(
        mock_db,
        SetBonusUserIdRequest(id=new_user.id),
        SetBonusRequest(count=bonus_count),
    )

    mock_get_user_by_id.assert_awaited_once_with(mock_db, new_user.id)
    assert isinstance(user, User)
    assert user.bonus == bonus_count
    assert user.id == new_user.id
    assert user.platform_id == new_user.platform_id
    assert user.first_name == new_user.first_name


@pytest.mark.asyncio
@patch("services.api.user.find_user_by_id.get_user_by_id")
async def test_set_bonus_when_user_not_exist(mock_get_user_by_id):
    """Проверяет обновление количества бонусов у не существующего пользователя"""
    user_id: int = random.randint(1, 100)
    bonus_count = random.randint(10, 100)
    mock_db = AsyncMock()
    mock_get_user_by_id.return_value = None
    with pytest.raises(UserNotFoundError):
        await set_bonus(
            mock_db,
            SetBonusUserIdRequest(id=user_id),
            SetBonusRequest(count=bonus_count),
        )
