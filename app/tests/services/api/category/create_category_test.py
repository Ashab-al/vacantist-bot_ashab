import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from models.category import Category
from services.api.category.create_category import create_category
from schemas.api.categories.create import CreateCategoryRequest


@pytest.mark.asyncio
async def test_create_category(session_factory):
    new_category_schema = CreateCategoryRequest(name="Тестовая категория")
    async with session_factory() as session:
        category: Category = await create_category(session, new_category_schema)
    assert new_category_schema.name == category.name
    assert category.id > 0