import random

import pytest
from models.category import Category
from sqlalchemy import select


@pytest.mark.asyncio
async def test_destroy_category(client, session):
    """Тестирует эндпоинт удаление категории по `id`"""
    category_name: str = f"Category {random.randint(1, 100)}"

    category = Category(name=category_name)
    session.add(category)
    await session.commit()
    await session.refresh(category)

    response = await client.delete(f"/categories/{category.id}")

    result_search_category: None = (
        await session.execute(select(Category).filter_by(name=category.name))
    ).scalar_one_or_none()
    assert result_search_category is None
    assert response.status_code == 200
    assert response.json().get("id") == category.id
    assert response.json().get("name") == category.name


@pytest.mark.asyncio
async def test_destroy_category_when_category_is_not_exist(client):
    """Тестирует эндпоинт удаление категории по не существующему `id`"""
    category_id: int = random.randint(1, 1000)

    response = await client.delete(f"/categories/{category_id}")

    assert response.status_code == 404
