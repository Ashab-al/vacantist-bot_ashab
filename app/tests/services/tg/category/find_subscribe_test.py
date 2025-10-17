import random
from unittest.mock import AsyncMock, patch

import pytest
from exceptions.user_not_found_error import UserNotFoundError
from models.category import Category
from models.user import User
from services.tg.category.find_subscribe import find_subscribe


@pytest.mark.asyncio
async def test_find_subscribe_mocked():
    """Проверяет поиск подписок пользователя"""
    random_count_categories: int = random.randint(1, 5)
    categories: list[Category] = [
        Category(id=i, name=f"cat_{i}") for i in range(random_count_categories)
    ]
    user_id = random.randint(1, 5)
    user_platform_id = random.randint(100, 200)
    fake_user: User = User(id=user_id, platform_id=user_platform_id, categories=categories)

    with patch(
        "services.tg.user.find_user_by_platform_id.get_user_by_platform_id",
        new_callable=AsyncMock,
    ) as mock_find_user:
        mock_find_user.return_value = fake_user

        result: list[Category] = await find_subscribe(db=None, user_data=fake_user)

        mock_find_user.assert_awaited_once_with(None, fake_user.platform_id)

        assert result == categories
        assert all(isinstance(cat, Category) for cat in result)


@pytest.mark.asyncio
async def test_find_subscribe_when_user_is_not_exist():
    """Проверяет поиск подписок у несуществующего пользователя"""
    random_count_categories: int = random.randint(1, 5)
    categories: list[Category] = [
        Category(id=i, name=f"cat_{i}") for i in range(random_count_categories)
    ]
    user_id = random.randint(1, 5)
    user_platform_id = random.randint(100, 200)
    fake_user = User(id=user_id, platform_id=user_platform_id, categories=categories)

    with patch(
        "services.tg.user.find_user_by_platform_id.get_user_by_platform_id",
        new_callable=AsyncMock,
    ) as mock_find_user:
        mock_find_user.return_value = None
        with pytest.raises(UserNotFoundError):
            await find_subscribe(db=None, user_data=fake_user)
        mock_find_user.assert_awaited_once_with(None, fake_user.platform_id)
