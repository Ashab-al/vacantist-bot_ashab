import pytest
from models.category import Category
from services.api.category.categories_list import categories_list
import random


@pytest.mark.asyncio
async def test_categories_list(
    session_factory
):
    """Проверяет, возвращаются ли корректно список категорий."""
    category_names: list[str] = [
        f"Category {random.randint(1, 1000)}" 
        for _ in range(4)
    ]
    async with session_factory() as session:
        for name in category_names:
            session.add(Category(name=name))
        await session.commit()
        result: list[Category] = await categories_list(session)

    assert len(result) == len(category_names)
    assert sorted([c.name for c in result]) == sorted(category_names)
    assert all(isinstance(category, Category) for category in result)


@pytest.mark.asyncio
async def test_categories_list_empty(
    session_factory
):
    """Проверяет, возвращаются ли пустой список."""
    empty_list_size: int = 0
    async with session_factory() as session:
        result: list[Category] = await categories_list(session)

    assert len(result) == empty_list_size