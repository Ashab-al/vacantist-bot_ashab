import random
from unittest.mock import AsyncMock, patch

import pytest
from exceptions.category.category_already_exist_error import CategoryAlreadyExistError
from models.category import Category
from schemas.api.categories.create import CreateCategoryRequest
from services.api.category.create_category import create_category
from tests.factories.category import CategoryFactory


@pytest.mark.asyncio
@patch("services.api.category.create_category.get_category_by_name")
async def test_create_category(mock_get_category_by_name):
    """Проверяет, что категория создаётся и сохраняется в базе данных."""
    mock_db = AsyncMock()
    category_name: str = CategoryFactory().name
    new_category_schema: CreateCategoryRequest = CreateCategoryRequest(
        name=category_name
    )
    mock_get_category_by_name.return_value = None
    category: Category = await create_category(mock_db, new_category_schema)

    mock_db.add.assert_called_once()
    mock_db.commit.assert_awaited_once()
    mock_db.refresh.assert_awaited_once_with(category)
    mock_get_category_by_name.assert_awaited_once_with(mock_db, category_name)
    assert isinstance(category, Category)
    assert new_category_schema.name == category.name
    assert category.name == category_name


@pytest.mark.asyncio
@patch("services.api.category.create_category.get_category_by_name")
async def test_create_existing_category(mock_get_category_by_name):
    """Проверяет, вызывает ли ошибка при попытке создать уже существующую категорию."""
    mock_db = AsyncMock()
    category_name: str = f"Category {random.randint(1, 1000)}"
    category: Category = Category(name=category_name)
    mock_get_category_by_name.return_value = category
    new_category_schema: CreateCategoryRequest = CreateCategoryRequest(
        name=category_name
    )
    with pytest.raises(CategoryAlreadyExistError):
        await create_category(mock_db, new_category_schema)
