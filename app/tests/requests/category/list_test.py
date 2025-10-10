import random

import pytest
from models.category import Category


@pytest.mark.asyncio
async def test_list_categories(client, session):
    """Тестирует эндпоинт возврата списка всех существующих категорий"""
    category_count = random.randint(4, 10)

    category_names: str = {f"Category {i}" for i in range(category_count)}
    categories: list[Category] = []
    for name in category_names:
        category = Category(name=name)
        session.add(category)
        await session.commit()
        await session.refresh(category)
        categories.append(category)

    response = await client.get("/categories/")

    assert response.status_code == 200
    assert len(response.json().get("categories")) == len(categories)
    assert {
        category.get("name") for category in response.json().get("categories")
    } == category_names
