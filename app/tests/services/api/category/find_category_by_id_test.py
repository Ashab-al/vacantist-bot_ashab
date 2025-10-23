import random
from unittest.mock import AsyncMock, patch

import pytest
from exceptions.category.category_not_found_error import CategoryNotFoundError
from models.category import Category
from schemas.api.categories.show.request import ShowCategoryRequest
from services.api.category.find_category_by_id import find_category_by_id
from tests.factories.category import CategoryFactory


@pytest.mark.asyncio
@patch("services.api.category.find_category_by_id.get_category_by_id")
async def test_find_category_by_id(mock_get_category_by_id):
    """Проверяет поиск категории по id"""
    mock_db = AsyncMock()

    category = CategoryFactory()
    mock_get_category_by_id.return_value = category

    find_category: Category = await find_category_by_id(
        mock_db, ShowCategoryRequest(id=category.id)
    )

    assert find_category is not None
    assert find_category.id == category.id
    assert find_category.name == category.name


@pytest.mark.asyncio
@patch("services.api.category.find_category_by_id.get_category_by_id")
async def test_find_not_exist_category_by_id(mock_get_category_by_id):
    """Проверяет поиск не существующей категории по id"""
    category_id: ShowCategoryRequest = ShowCategoryRequest(id=random.randint(1, 1000))
    mock_db = AsyncMock()
    mock_get_category_by_id.return_value = None
    with pytest.raises(CategoryNotFoundError):
        await find_category_by_id(mock_db, category_id)
