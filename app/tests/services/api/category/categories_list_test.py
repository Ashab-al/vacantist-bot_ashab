import random
from unittest.mock import AsyncMock, patch

import pytest
from models.category import Category
from services.api.category.categories_list import categories_list
from tests.factories.category import CategoryFactory


@pytest.mark.asyncio
@patch("services.api.category.categories_list.get_all_categories")
async def test_categories_list(mock_get_all_categories):
    """Проверяет, возвращаются ли корректно список категорий."""
    mock_db = AsyncMock()
    categories_count: int = random.randint(1, 10)
    categories = [CategoryFactory() for _ in range(categories_count)]
    mock_get_all_categories.return_value = categories
    result: list[Category] = await categories_list(mock_db)

    mock_get_all_categories.assert_awaited_once_with(mock_db)
    assert len(result) == categories_count
    assert all(isinstance(category, Category) for category in result)


@pytest.mark.asyncio
@patch("services.api.category.categories_list.get_all_categories")
async def test_categories_list_empty(mock_get_all_categories):
    """Проверяет, возвращается ли пустой список."""
    mock_db = AsyncMock()
    empty_list_size: int = 0
    mock_get_all_categories.return_value = []
    result: list[Category] = await categories_list(mock_db)

    mock_get_all_categories.assert_awaited_once_with(mock_db)
    assert len(result) == empty_list_size
