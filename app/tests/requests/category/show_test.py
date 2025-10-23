import random
from unittest.mock import patch

import pytest
from fastapi import status
from models.category import Category
from tests.factories.category import CategoryFactory


@pytest.mark.asyncio
@patch("services.api.category.find_category_by_id.get_category_by_id")
async def test_show_category(mock_get_category_by_id, client):
    """Тестирует эндпоинт возврата категории по id категории"""
    category: Category = CategoryFactory()
    mock_get_category_by_id.return_value = category
    response = await client.get(f"/categories/{category.id}")

    assert response.status_code == status.HTTP_200_OK
    assert response.json().get("name") == category.name


@pytest.mark.asyncio
@patch("services.api.category.find_category_by_id.get_category_by_id")
async def test_show_category_when_category_is_not_exist(
    mock_get_category_by_id, client
):
    """Тестирует эндпоинт возврата категории по id категории когда категории не существует"""

    category_id: int = random.randint(1, 10)
    mock_get_category_by_id.return_value = None
    response = await client.get(f"/categories/{category_id}")

    assert response.status_code == status.HTTP_404_NOT_FOUND
