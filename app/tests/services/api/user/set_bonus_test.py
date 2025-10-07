import pytest
from models.user import User
from services.api.user.set_bonus import set_bonus
import random
from schemas.api.users.set_bonus.request import SetBonusUserIdRequest, SetBonusRequest


@pytest.mark.asyncio
async def test_set_bonus(
    session_factory,
    new_tg_user: User
):
    """Проверяет обновление количества бонусов у пользователя"""
    bonus_count = random.randint(10, 100)

    async with session_factory() as session:
        user: User = await set_bonus(
            session,
            SetBonusUserIdRequest(id=new_tg_user.id),
            SetBonusRequest(count=bonus_count)
        )
    
    assert isinstance(user, User)
    assert user.bonus == bonus_count
    assert user.id == new_tg_user.id
    assert user.platform_id == new_tg_user.platform_id
    assert user.first_name == new_tg_user.first_name


@pytest.mark.asyncio
async def test_set_bonus_when_user_not_exist(
    session_factory
):
    """Проверяет обновление количества бонусов у не существующего пользователя"""
    user_id: int = random.randint(1, 100)
    bonus_count = random.randint(10, 100)

    with pytest.raises(
        ValueError, 
        match=f"Пользователя по id - {user_id} нет в базе"
    ):
        async with session_factory() as session:
            await set_bonus(
                session,
                SetBonusUserIdRequest(id=user_id),
                SetBonusRequest(count=bonus_count)
            )
    