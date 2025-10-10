import pytest
from models.category import Category
from services.api.category.find_category_by_id import find_category_by_id
import random
from schemas.api.categories.show.request import ShowCategoryRequest


@pytest.mark.asyncio
async def test_find_category_by_id(session):
    """Проверяет поиск категории по id"""
    category_name: str = f"Category {random.randint(1, 1000)}"

    category = Category(name=category_name)
    session.add(category)
    await session.commit()
    await session.refresh(category)

    find_category: Category = await find_category_by_id(
        session, ShowCategoryRequest(id=category.id)
    )

    assert find_category is not None
    assert find_category.id == category.id
    assert find_category.name == category.name


@pytest.mark.asyncio
async def test_find_not_exist_category_by_id(session):
    """Проверяет поиск не существующей категории по id"""
    category_id: ShowCategoryRequest = ShowCategoryRequest(id=random.randint(1, 1000))

    with pytest.raises(ValueError) as excinfo:
        await find_category_by_id(session, category_id)

    assert excinfo.type is ValueError
    assert f"Категории по id - {category_id.id} нет в базе" in str(excinfo.value)
