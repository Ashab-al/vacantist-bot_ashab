import pytest
from models.user import User
from services.api.user.find_user_by_id import find_user_by_id
import random
from schemas.api.users.show.request import ShowUserRequest


@pytest.mark.asyncio
async def test_find_user_by_id(session, new_tg_user: User):
    """Проверяет поиск пользователя по id"""

    user: User = await find_user_by_id(session, ShowUserRequest(id=new_tg_user.id))

    assert isinstance(user, User)
    assert user.id == new_tg_user.id
    assert user.platform_id == new_tg_user.platform_id
    assert user.first_name == new_tg_user.first_name


@pytest.mark.asyncio
async def test_find_user_by_id_when_user_not_exist(session):
    """Проверяет поиск не существующего пользователя по id"""
    user_id: int = random.randint(1, 100)

    with pytest.raises(ValueError, match=f"Пользователя по id - {user_id} нет в базе"):
        await find_user_by_id(session, ShowUserRequest(id=user_id))
