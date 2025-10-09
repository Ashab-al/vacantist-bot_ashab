import random
import pytest
from tests.conftest import create_tg_user
from models.user import User
from enums.bot_status_enum import BotStatusEnum


@pytest.mark.asyncio
async def test_show(
    client, 
    session
):
    """Тестирует эндпоинт который возвращает данные о пользователе"""
    user: User = await create_tg_user(session)
        
    response = await client.get(
        f"/users/{user.id}"
    )

    assert response.status_code == 200
    assert response.json().get('id') == user.id
    assert response.json().get('platformId') == user.platform_id
    assert response.json().get('botStatus') == BotStatusEnum.WORKS.value


@pytest.mark.asyncio
async def test_show_when_user_is_not_exist(
    client
):
    """Тестирует эндпоинт который вовзращает ошибку, если пользователь не существует"""
    user_id: int = random.randint(1, 100)
        
    response = await client.get(
        f"/users/{user_id}"
    )

    assert response.status_code == 404
    assert response.json().get('detail') == f"Пользователя по id - {user_id} нет в базе"

