import random
from unittest.mock import AsyncMock, patch

import pytest
from exceptions.category.category_not_found_error import CategoryNotFoundError
from models.category import Category
from schemas.api.categories.update.request import UpdateCategoryRequest
from services.api.category.update_category import update_category
from tests.factories.category import CategoryFactory


@pytest.mark.asyncio
@patch("services.api.category.update_category.get_category_by_id")
async def test_update_category(mock_get_category_by_id):
    """Проверяет обновление названия категории"""
    mock_db = AsyncMock()
    new_category_name: str = f"Category {random.randint(101, 200)}"

    category = CategoryFactory()
    mock_get_category_by_id.return_value = category
    update_category_name: Category = await update_category(
        mock_db, category.id, UpdateCategoryRequest(name=new_category_name)
    )

    mock_get_category_by_id.assert_awaited_once_with(mock_db, category.id)
    assert isinstance(update_category_name, Category)
    assert update_category_name.id == category.id
    assert update_category_name.name == new_category_name


@pytest.mark.asyncio
@patch("services.api.category.update_category.get_category_by_id")
async def test_update_category_when_category_is_not_exist(mock_get_category_by_id):
    """Проверяет обновления названия не существующей категории"""
    mock_db = AsyncMock()
    mock_get_category_by_id.return_value = None
    category_id: int = random.randint(1, 1000)
    new_category_name: str = f"Category {random.randint(1, 200)}"

    with pytest.raises(CategoryNotFoundError):
        await update_category(
            mock_db, category_id, UpdateCategoryRequest(name=new_category_name)
        )
