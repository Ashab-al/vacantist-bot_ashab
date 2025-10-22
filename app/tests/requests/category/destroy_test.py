import random
from unittest.mock import patch

import pytest
from fastapi import status
from tests.factories.category import CategoryFactory


@pytest.mark.asyncio
@patch("services.api.category.delete_category.get_category_by_id")
async def test_destroy_category(mock_get_category_by_id, client, session_mock):
    """Тестирует эндпоинт удаление категории по `id`"""

    category = CategoryFactory()
    mock_get_category_by_id.return_value = category
    response = await client.delete(f"/categories/{category.id}")

    session_mock.delete.assert_awaited_once_with(category)
    assert response.status_code == status.HTTP_200_OK
    assert response.json().get("id") == category.id
    assert response.json().get("name") == category.name


@pytest.mark.asyncio
@patch("services.api.category.delete_category.get_category_by_id")
async def test_destroy_category_when_category_is_not_exist(
    mock_get_category_by_id, client
):
    """Тестирует эндпоинт удаление категории по не существующему `id`"""
    category_id: int = random.randint(1, 1000)
    mock_get_category_by_id.return_value = None
    response = await client.delete(f"/categories/{category_id}")

    assert response.status_code == status.HTTP_404_NOT_FOUND
