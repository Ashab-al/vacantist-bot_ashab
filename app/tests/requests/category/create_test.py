import random

import pytest
from models.category import Category
from sqlalchemy import select


@pytest.mark.asyncio
async def test_create_category(client, session):
    """Тестирует эндпоинт создания новой категории."""
    category_name: str = f"Category {random.randint(1, 100)}"
    data: dict[str, str] = {"name": category_name}
    first_id: int = 1

    response = await client.post("/categories/", json=data)
    category: Category = (
        (await session.execute(select(Category).where(Category.name == category_name)))
        .scalars()
        .one_or_none()
    )

    assert response.status_code == 200
    assert response.json().get("id") == first_id
    assert response.json().get("name") == category_name
    assert category.name == response.json().get("name")
    assert category.id == response.json().get("id")


@pytest.mark.asyncio
async def test_create_category_when_category_is_exist(client, session):
    """Тестирует эндпоинт создания категории когда такая категория уже существует."""
    category_name: str = f"Category {random.randint(1, 100)}"
    data: dict[str, str] = {"name": category_name}
    category = Category(name=category_name)
    session.add(category)
    await session.commit()

    response = await client.post("/categories/", json=data)
    assert response.status_code == 400
    assert response.json().get("detail") == "Такая категория уже существует"
