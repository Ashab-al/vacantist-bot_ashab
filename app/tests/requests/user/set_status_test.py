import random

import pytest
from enums.bot_status_enum import BotStatusEnum
from models.user import User
from tests.conftest import create_tg_user


@pytest.mark.asyncio
async def test_set_status(client, session):
    """Тестирует эндпоинт обновления статуса у пользователя"""
    user: User = await create_tg_user(session)

    response = await client.post(
        f"/users/{user.id}/set_status",
        json={"bot_status": BotStatusEnum.BOT_BLOCKED.value},
    )

    assert response.status_code == 200
    assert response.json().get("botStatus") == BotStatusEnum.BOT_BLOCKED.value


@pytest.mark.asyncio
async def test_set_status_when_user_is_not_exist(client):
    """Тестирует эндпоинт обновления статуса у пользователя, которого не существует"""
    user_id: int = random.randint(1, 100)

    response = await client.post(
        f"/users/{user_id}/set_status",
        json={"bot_status": BotStatusEnum.BOT_BLOCKED.value},
    )

    assert response.status_code == 404
    # assert response.json().get("detail") == f"Пользователя по id - {user_id} нет в базе"
