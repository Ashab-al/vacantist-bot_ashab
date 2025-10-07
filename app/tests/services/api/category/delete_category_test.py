import pytest
from models.category import Category
from services.api.category.delete_category import delete_category
import random
from schemas.api.categories.destroy import DestroyCategoryRequest


@pytest.mark.asyncio
async def test_delete_category(
    session_factory
):
    """Проверяет удаление категории по id"""
    category_name: str = f"Category {random.randint(1, 1000)}"
    
    async with session_factory() as session:
        category = Category(name = category_name)
        session.add(category)
        await session.commit()
        await session.refresh(category)

        destroy_category_request = DestroyCategoryRequest(id=category.id)
        result_delete: Category = await delete_category(session, destroy_category_request)

        find_category: None | Category = await session.get(Category, category.id)
    
    assert find_category is None
    assert result_delete.id == category.id
    assert result_delete.name == category.name
    
@pytest.mark.asyncio
async def test_delete_not_exist_category(
    session_factory
):
    """Проверяет удаление не существующей категории"""
    category_id: int = random.randint(1, 1000)
    destroy_category_request: DestroyCategoryRequest = DestroyCategoryRequest(id=category_id)

    with pytest.raises(ValueError) as excinfo:
        async with session_factory() as session:
            await delete_category(session, destroy_category_request)
    
    assert excinfo.type is ValueError
    assert "Категории не существует" in str(excinfo.value)