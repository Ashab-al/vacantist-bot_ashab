import random
from unittest.mock import AsyncMock, patch

import pytest
from exceptions.category.category_not_found_error import CategoryNotFoundError
from models.category import Category
from schemas.api.categories.destroy import DestroyCategoryRequest
from services.api.category.delete_category import delete_category
from tests.factories.category import CategoryFactory


@pytest.mark.asyncio
@patch("services.api.category.delete_category.get_category_by_id")
async def test_delete_category(mock_get_category_by_id):
    """Проверяет удаление категории по id"""
    mock_db = AsyncMock()
    category = CategoryFactory()
    mock_get_category_by_id.return_value = category

    destroy_category_request = DestroyCategoryRequest(id=category.id)
    result_delete: Category = await delete_category(mock_db, destroy_category_request)

    mock_get_category_by_id.assert_awaited_once_with(mock_db, category.id)
    assert result_delete.id == category.id
    assert result_delete.name == category.name


@pytest.mark.asyncio
@patch("services.api.category.delete_category.get_category_by_id")
async def test_delete_not_exist_category(mock_get_category_by_id):
    """Проверяет удаление не существующей категории"""
    mock_db = AsyncMock()
    category_id: int = random.randint(1, 1000)
    destroy_category_request: DestroyCategoryRequest = DestroyCategoryRequest(
        id=category_id
    )
    mock_get_category_by_id.return_value = None

    with pytest.raises(CategoryNotFoundError):
        await delete_category(mock_db, destroy_category_request)
