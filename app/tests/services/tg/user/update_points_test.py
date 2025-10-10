import random

import pytest
from aiogram.types import User as AiogramTgUser
from enums.bot_status_enum import BotStatusEnum
from models.user import User
from services.tg.user.update_points import update_points


@pytest.mark.asyncio
async def test_update_points(session, new_tg_user):
    """Проверяет обновление количества поинтов"""
    is_bot: bool = False
    count_points: int = random.randint(3, 100)
    aiogram_user: AiogramTgUser = AiogramTgUser(
        id=new_tg_user.platform_id,
        is_bot=is_bot,
        first_name=new_tg_user.first_name,
        username=new_tg_user.username,
    )
    user: User = await update_points(session, aiogram_user, count_points)

    assert user.point == count_points
    assert user.bot_status == BotStatusEnum.WORKS
    assert user.platform_id == new_tg_user.platform_id
    assert user.id == new_tg_user.id


@pytest.mark.asyncio
async def test_update_points_when_user_is_not_exist(session):
    """Проверяет обновление количества поинтов у несуществующего пользователя"""
    user_id = random.randint(1, 1000)
    is_bot = False
    first_name = "Тестовый"
    username = "test_user"
    count_points: int = random.randint(3, 100)
    aiogram_user = AiogramTgUser(
        id=user_id, is_bot=is_bot, first_name=first_name, username=username
    )
    with pytest.raises(
        ValueError, match=f"Пользователь с platform_id {user_id} не найден"
    ):
        await update_points(session, aiogram_user, count_points)
