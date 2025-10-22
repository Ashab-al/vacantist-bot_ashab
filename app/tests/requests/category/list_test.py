import random
from unittest.mock import patch

import pytest
from fastapi import status
from models.category import Category
from tests.factories.category import CategoryFactory


@pytest.mark.asyncio
@patch("api.categories.list.ListCategoryResponse")
@patch("services.api.category.categories_list.get_all_categories")
async def test_list_categories(
    mock_get_all_categories, mock_list_category_response, client
):
    """Тестирует эндпоинт возврата списка всех существующих категорий"""
    category_count = random.randint(4, 10)

    categories: list[Category] = [CategoryFactory() for _ in range(category_count)]

    mock_get_all_categories.return_value = categories
    mock_list_category_response.return_value = {"categories": categories}
    response = await client.get("/categories/")

    assert response.status_code == status.HTTP_200_OK
    assert len(response.json().get("categories")) == len(categories)
