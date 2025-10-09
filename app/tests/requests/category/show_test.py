import random
import pytest
from models.category import Category


@pytest.mark.asyncio
async def test_show_category(
    client, 
    session
):
    """Тестирует эндпоинт возврата категории по id категории"""

    category_name: str = f"Category {random.randint(4, 10)}"
    category = Category(name=category_name)
    session.add(category)
    await session.commit()
    await session.refresh(category)
    
    response = await client.get(
        f"/categories/{category.id}"
    )

    assert response.status_code == 200
    assert response.json().get('name') == category_name
    assert response.json().get('id') == category.id


@pytest.mark.asyncio
async def test_show_category_when_category_is_not_exist(
    client
):
    """Тестирует эндпоинт возврата категории по id категории когда категории не существует"""

    category_id: int = random.randint(1, 10)
    
    response = await client.get(
        f"/categories/{category_id}"
    )

    assert response.status_code == 404
    assert response.json().get('detail') == f"Категории по id - {category_id} нет в базе"