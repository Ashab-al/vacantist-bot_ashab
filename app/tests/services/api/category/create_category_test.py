import pytest
from sqlalchemy import select
from models.category import Category
from services.api.category.create_category import create_category
from schemas.api.categories.create import CreateCategoryRequest
import random


@pytest.mark.asyncio
async def test_create_category(session_factory):
    """Проверяет, что категория создаётся и сохраняется в базе данных."""
    category_name: str = f"Category {random.randint(1, 1000)}"
    new_category_schema: CreateCategoryRequest = CreateCategoryRequest(name=category_name)
    
    async with session_factory() as session:
        category: Category = await create_category(session, new_category_schema)
    
    async with session_factory() as session:
        result = await session.execute(select(Category).filter_by(id=category.id))
        saved: Category = result.scalar_one()

    assert isinstance(category, Category)
    assert new_category_schema.name == category.name
    assert category.id > 0
    assert saved.name == category_name


@pytest.mark.asyncio
async def test_create_existing_category(session_factory):
    """Проверяет, вызывает ли ошибка при попытке создать уже существующую категорию."""
    category_name: str = f"Category {random.randint(1, 1000)}"
    async with session_factory() as session:
        category: Category = Category(name=category_name)
        session.add(category)
        await session.commit()
        await session.refresh(category)
    
    new_category_schema: CreateCategoryRequest = CreateCategoryRequest(name=category_name)
    with pytest.raises(ValueError) as excinfo:
        async with session_factory() as session:
            await create_category(session, new_category_schema)
    
    assert excinfo.type is ValueError
    assert "Такая категория уже существует" in str(excinfo.value)