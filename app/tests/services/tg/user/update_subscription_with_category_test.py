import random
from unittest.mock import AsyncMock

import pytest
from bot.filters.callback.category_callback import CategoryCallback
from enums.category_subscription_enum import CategorySubscriptionEnum
from models.category import Category
from models.user import User
from services.tg.user.update_subscription_with_category import (
    update_subscription_with_category,
)


@pytest.mark.asyncio
async def test_update_subscription_with_category_when_user_has_subscribe(mocker):
    """
    Проверка подписки / отписки на категорию.
    Случай когда пользователь изначально был подписан на категорию
    """
    platform_id: int = random.randint(1000, 2000)
    user_id: int = random.randint(1, 1000)
    subscribe_count: int = random.randint(3, 10)
    categories: list[Category] = [
        Category(id=i, name=f"cat_{i}") for i in range(subscribe_count)
    ]
    category_callback: CategoryCallback = CategoryCallback(category_id=categories[0].id)
    mock_get_category_by_id = mocker.patch(
        "services.tg.user.update_subscription_with_category.get_category_by_id",
        return_value=categories[0],
    )
    mock_db = AsyncMock()

    new_user: User = User(id=user_id, platform_id=platform_id, categories=[])

    new_user.categories.extend(categories)

    result: CategorySubscriptionEnum = await update_subscription_with_category(
        category_callback, mock_db, new_user.categories, new_user
    )
    mock_get_category_by_id.assert_awaited_once_with(
        mock_db, category_callback.category_id
    )
    mock_db.commit.assert_awaited_once()
    assert result == CategorySubscriptionEnum.UNSUBSCRIBE


@pytest.mark.asyncio
async def test_update_subscription_with_category_when_user_has_not_subscribe(mocker):
    """
    Проверка подписки / отписки на категорию.
    Случай когда пользователь изначально не был подписан на категорию
    """
    platform_id: int = random.randint(1000, 2000)
    user_id: int = random.randint(1, 1000)
    subscribe_count: int = random.randint(3, 10)
    categories: list[Category] = [
        Category(id=i, name=f"cat_{i}") for i in range(subscribe_count)
    ]
    category_callback: CategoryCallback = CategoryCallback(category_id=categories[0].id)
    mock_get_category_by_id = mocker.patch(
        "services.tg.user.update_subscription_with_category.get_category_by_id",
        return_value=categories[0],
    )
    mock_db = AsyncMock()

    new_user: User = User(id=user_id, platform_id=platform_id, categories=[])

    result: CategorySubscriptionEnum = await update_subscription_with_category(
        category_callback, mock_db, new_user.categories, new_user
    )
    mock_get_category_by_id.assert_awaited_once_with(
        mock_db, category_callback.category_id
    )
    mock_db.commit.assert_awaited_once()
    assert new_user.categories[0] == categories[0]
    assert len(new_user.categories) == 1
    assert result == CategorySubscriptionEnum.SUBSCRIBE
