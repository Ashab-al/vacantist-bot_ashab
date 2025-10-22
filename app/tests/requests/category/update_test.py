import random

import pytest
from models.category import Category


@pytest.mark.asyncio
async def test_update_category(client, session):
    """Тестирует эндпоинт обновления названия категории по id категории"""

    category_name: str = f"Category {random.randint(1, 10)}"
    new_category_name: str = f"Category {random.randint(11, 20)}"
    category = Category(name=category_name)
    session.add(category)
    await session.commit()
    await session.refresh(category)

    response = await client.patch(
        f"/categories/{category.id}", json={"name": new_category_name}
    )

    assert response.status_code == 200
    assert response.json().get("name") == new_category_name
    assert response.json().get("id") == category.id


@pytest.mark.asyncio
async def test_update_category_when_category_is_not_exist(client):
    """Тестирует эндпоинт обновления названия категории по id которого нет в базе"""

    category_id: int = random.randint(1, 10)
    new_category_name: str = f"Category {random.randint(11, 20)}"

    response = await client.patch(
        f"/categories/{category_id}", json={"name": new_category_name}
    )

    assert response.status_code == 404


@pytest.mark.asyncio
async def test_update_category_when_data_is_not_correct(client, session):
    """Тестирует эндпоинт обновления названия категории передавая некорректное название"""

    category_name: str = f"Category {random.randint(1, 10)}"
    new_category_name: int = random.randint(1000, 100000)
    category = Category(name=category_name)
    session.add(category)
    await session.commit()
    await session.refresh(category)

    response = await client.patch(
        f"/categories/{category.id}", json={"name": new_category_name}
    )

    assert response.status_code == 422
