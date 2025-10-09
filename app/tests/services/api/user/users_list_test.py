import pytest
from models.user import User
from services.api.user.users_list import users_list
import random
from tests.conftest import create_tg_user


@pytest.mark.asyncio
async def test_users_list(session):
    """Проверяет получение списка пользователей"""
    user_count = random.randint(3, 10)

    for _ in range(user_count):
        await create_tg_user(session)

    user_list: list[User] = await users_list(session)

    assert len(user_list) == user_count
    assert all(isinstance(user, User) for user in user_list)
