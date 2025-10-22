import random
from unittest.mock import AsyncMock, patch

import pytest
from fastapi import status
from httpx import AsyncClient
from models.category import Category
from sqlalchemy import select
from tests.factories.category import CategoryFactory


@pytest.mark.asyncio
@patch("services.api.category.create_category.get_category_by_name")
async def test_create_category(mock_get_category_by_name, client: AsyncClient):
    """Тестирует эндпоинт создания новой категории."""

    category: Category = CategoryFactory()
    category_name: str = category.name
    data: dict[str, str] = {"name": category.name}
    mock_get_category_by_name.return_value = None
    response = await client.post("/categories/", json=data)

    assert response.status_code == status.HTTP_200_OK
    assert response.json().get("name") == category_name
    assert category.name == response.json().get("name")


@pytest.mark.asyncio
@patch("services.api.category.create_category.get_category_by_name")
async def test_create_category_when_category_is_exist(
    mock_get_category_by_name, client: AsyncClient
):
    """Тестирует эндпоинт создания категории когда такая категория уже существует."""
    category = CategoryFactory()
    mock_get_category_by_name.return_value = category

    data: dict[str, str] = {"name": category.name}
    response = await client.post("/categories/", json=data)
    assert response.status_code == 400
    assert response.json().get("detail") == "Такая категория уже существует"
