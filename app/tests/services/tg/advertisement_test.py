import random

import pytest
from models.category import Category
from services.tg.advertisement import advertisement
from tests.factories.category import CategoryFactory
from unittest.mock import AsyncMock, Mock

@pytest.mark.asyncio
async def test_advertisement():
    """Тестирует получение списка категорий с количеством пользователей"""
    one_user: int = 1
    subscribe_count: int = random.randint(3, 10)
    categories: list[Category] = [
        CategoryFactory() for _ in range(subscribe_count)
    ]

    mock_db = AsyncMock()
    mock_all = Mock()
    mock_all.all.return_value = [
        (category.name, one_user) for category in categories
    ]
    mock_db.execute.return_value = mock_all

    result: list[tuple[str, int]] = await advertisement(mock_db)

    assert len(result) == subscribe_count
    assert {category_name for category_name, _ in result} == {
        category.name for category in categories
    }
    assert all(user_count == one_user for _, user_count in result)
