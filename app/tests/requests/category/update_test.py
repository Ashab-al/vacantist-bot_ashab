import random
from unittest.mock import patch

import pytest
from fastapi import status
from models.category import Category
from tests.factories.category import CategoryFactory


@pytest.mark.asyncio
@patch("services.api.category.update_category.get_category_by_id")
async def test_update_category(mock_get_category_by_id, client):
    """Тестирует эндпоинт обновления названия категории по id категории"""

    new_category_name: str = f"Category {random.randint(11, 20)}"
    category = CategoryFactory()
    mock_get_category_by_id.return_value = category
    response = await client.patch(
        f"/categories/{category.id}", json={"name": new_category_name}
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json().get("name") == new_category_name
    assert response.json().get("id") == category.id


@pytest.mark.asyncio
@patch("services.api.category.update_category.get_category_by_id")
async def test_update_category_when_category_is_not_exist(
    mock_get_category_by_id, client
):
    """Тестирует эндпоинт обновления названия категории по id которого нет в базе"""

    category_id: int = random.randint(1, 10)
    new_category_name: str = f"Category {random.randint(11, 20)}"
    mock_get_category_by_id.return_value = None
    response = await client.patch(
        f"/categories/{category_id}", json={"name": new_category_name}
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_update_category_when_data_is_not_correct(client):
    """Тестирует эндпоинт обновления названия категории передавая некорректное название"""

    category_name: str = f"Category {random.randint(1, 10)}"
    new_category_name: int = random.randint(1000, 100000)
    category = Category(name=category_name)

    response = await client.patch(
        f"/categories/{category.id}", json={"name": new_category_name}
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
