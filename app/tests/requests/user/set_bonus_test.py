import random

import pytest
from models.user import User
from tests.conftest import create_tg_user


@pytest.mark.asyncio
async def test_set_bonus(client, session):
    """Тестирует эндпоинт обновления количество бонусов у пользователя"""
    bonus_count: int = random.randint(1, 100)
    user: User = await create_tg_user(session)

    response = await client.post(
        f"/users/{user.id}/set_bonus", json={"count": bonus_count}
    )

    assert response.status_code == 200
    assert response.json().get("bonus") == bonus_count


@pytest.mark.asyncio
async def test_set_bonus_when_user_is_not_exist(client):
    """Тестирует эндпоинт обновления количество бонусов у пользователя, которого не существует"""
    bonus_count: int = random.randint(1, 100)
    user_id: int = random.randint(1, 100)

    response = await client.post(
        f"/users/{user_id}/set_bonus", json={"count": bonus_count}
    )

    assert response.status_code == 404
    # assert response.json().get("detail") == f"Пользователя по id - {user_id} нет в базе"
