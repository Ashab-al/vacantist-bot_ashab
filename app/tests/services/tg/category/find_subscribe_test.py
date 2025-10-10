import random

import pytest
from models.category import Category
from models.user import User
from repositories.users.get_user_by_id import get_user_by_id
from schemas.tg.user.tg_user import TgUser
from services.tg.category.find_subscribe import find_subscribe
from tests.conftest import (create_tg_user_with_session,
                            create_vacancy_and_category_with_session)


@pytest.mark.asyncio
async def test_find_subscribe(session):
    """Проверяет поиск подписок пользователя"""
    subscribe_count: int = random.randint(3, 10)
    categories = []
    for _ in range(subscribe_count):
        _vacancy, category = await create_vacancy_and_category_with_session(session)
        categories.append(category)

    user: User = await get_user_by_id(
        session, user_id=(await create_tg_user_with_session(session)).id
    )

    user.categories.extend(categories)

    await session.commit()

    subscribes: list[Category] = await find_subscribe(session, user)

    assert len(subscribes) == len(categories)
    assert len(subscribes) == subscribe_count
    assert all(isinstance(category, Category) for category in subscribes)


@pytest.mark.asyncio
async def test_find_subscribe_when_user_is_not_exist(session):
    """Проверяет поиск подписок у несуществующего пользователя"""
    user_id: int = random.randint(1, 100)

    with pytest.raises(ValueError, match="Пользователь не найден"):
        user_data: dict[str, str | int] = {
            "id": random.randint(1000, 100000000),
            "first_name": f"Имя {random.randint(1, 1000)}",
            "username": f"asd{random.randint(1, 1000)}",
        }
        new_user_schema: TgUser = TgUser.model_validate(user_data)
        user: User = User(
            platform_id=new_user_schema.id,
            first_name=new_user_schema.first_name,
            username=new_user_schema.username,
            email=new_user_schema.email,
            phone=new_user_schema.phone,
            point=new_user_schema.point,
            bonus=new_user_schema.bonus,
            bot_status=new_user_schema.bot_status,
        )
        user.id = user_id

        await find_subscribe(session, user)
