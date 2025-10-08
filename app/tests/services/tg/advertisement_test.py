import random
import pytest
from models.category import Category
from models.user import User
from repositories.users.get_user_by_id import get_user_by_id
from schemas.api.categories.create.request import CreateCategoryRequest
from services.api.category.create_category import create_category
from tests.conftest import create_tg_user_with_session
from services.tg.advertisement import advertisement

@pytest.mark.asyncio
async def test_advertisement(session_factory):
    one_user: int = 1
    async with session_factory() as session:
        subscribe_count: int = random.randint(3, 10)
        categories: list[Category] = []
        for _ in range(subscribe_count):
            category_name: str = f"Category {random.randint(1, 10000000000)}"
            category: Category = await create_category(
                session, 
                CreateCategoryRequest(name = category_name)
            )
            categories.append(category)

        user: User = await get_user_by_id(
            session, 
            user_id=(await create_tg_user_with_session(session)).id
        )
        user.categories.extend(categories)
        await session.commit()

        result: list[tuple[str, int]] = await advertisement(session)
    
    assert len(result) == subscribe_count
    assert {category_name for category_name, _ in result} == {category.name for category in categories}
    assert all(user_count == one_user for _, user_count in result)
