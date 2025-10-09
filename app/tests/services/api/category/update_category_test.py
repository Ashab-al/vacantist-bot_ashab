import pytest
from models.category import Category
from services.api.category.update_category import update_category
import random
from schemas.api.categories.update.request import UpdateCategoryRequest


@pytest.mark.asyncio
async def test_update_category(
    session
):
    """Проверяет обновление названия категории"""
    category_name: str = f"Category {random.randint(1, 100)}"
    new_category_name: str = f"Category {random.randint(101, 200)}"
    
    category = Category(name = category_name)
    session.add(category)
    await session.commit()
    await session.refresh(category)

    update_category_name: Category = await update_category(
        session, 
        category.id,
        UpdateCategoryRequest(name=new_category_name)
    )

    find_category: Category = await session.get(
        Category, 
        category.id
    )

    assert isinstance(update_category_name, Category)
    assert update_category_name.id == category.id
    assert update_category_name.name == new_category_name

    assert find_category.id == category.id
    assert find_category.name == new_category_name

@pytest.mark.asyncio
async def test_update_category_when_category_is_not_exist(
    session
):
    """Проверяет обновления названия не существующей категории"""
    category_id: int = random.randint(1, 1000)
    new_category_name: str = f"Category {random.randint(1, 200)}"

    with pytest.raises(ValueError) as excinfo:
        await update_category(
            session, 
            category_id,
            UpdateCategoryRequest(name=new_category_name)
        )
    
    assert excinfo.type is ValueError
    assert f"Категории по id - {category_id} нет в базе" in str(excinfo.value)