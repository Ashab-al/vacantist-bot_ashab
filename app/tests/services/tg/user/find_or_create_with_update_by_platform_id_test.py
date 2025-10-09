import pytest
from aiogram.types import User as AiogramTgUser
from sqlalchemy import select
import random
from models.user import User
from enums.bot_status_enum import BotStatusEnum
from services.tg.user.find_or_create_with_update_by_platform_id import find_or_create_with_update_by_platform_id


@pytest.mark.asyncio
async def test_find_or_create_creates_new_user(session, mocker):
    """Создает нового пользователя, если его нет в базе"""
    
    user_id = random.randint(1, 1000)
    is_bot = False
    first_name = "Тестовый"
    username = "test_user"
    
    # Мокаем send_analytics, чтобы не дергать реальную отправку
    mock_send_analytics = mocker.patch(
        "services.tg.user.find_or_create_with_update_by_platform_id.send_analytics"
    )

    aiogram_user = AiogramTgUser(
        id=user_id,
        is_bot=is_bot,
        first_name=first_name,
        username=username
    )

    user = await find_or_create_with_update_by_platform_id(session, aiogram_user)

    assert user.id is not None
    assert user.platform_id == user_id
    assert user.first_name == first_name
    assert user.bot_status == BotStatusEnum.WORKS
    mock_send_analytics.assert_awaited_once_with(session, user)

    # Проверяем, что пользователь реально записан в БД
    result = await session.execute(select(User).where(User.platform_id == user_id))
    db_user = result.scalar_one()
    assert db_user is not None


@pytest.mark.asyncio
async def test_find_or_create_returns_existing_user(session, mocker):
    """Возвращает пользователя, если он уже существует и активен"""
    user_id = random.randint(1, 1000)
    is_bot = False
    first_name = "Уже"
    username = "existing"
    
    user = User(
        platform_id=user_id,
        first_name=first_name,
        username=username,
        bot_status=BotStatusEnum.WORKS,
    )
    session.add(user)
    await session.commit()

    mock_send_analytics = mocker.patch(
        "services.tg.user.find_or_create_with_update_by_platform_id.send_analytics"
    )

    aiogram_user = AiogramTgUser(id=user_id, is_bot=is_bot, first_name=first_name, username=username)

    result_user = await find_or_create_with_update_by_platform_id(session, aiogram_user)

    assert result_user.id == user.id
    assert result_user.bot_status == BotStatusEnum.WORKS
    mock_send_analytics.assert_not_awaited()


@pytest.mark.asyncio
async def test_find_or_create_unblocks_user(session, mocker):
    """Обновляет статус пользователя с BOT_BLOCKED на WORKS"""
    user_id = random.randint(1, 1000)
    is_bot = False
    first_name = "Блокированный"
    username = "blocked_user"
    user = User(
        platform_id=user_id,
        first_name=first_name,
        username=username,
        bot_status=BotStatusEnum.BOT_BLOCKED,
    )
    session.add(user)
    await session.commit()

    mock_send_analytics = mocker.patch(
        "services.tg.user.find_or_create_with_update_by_platform_id.send_analytics"
    )

    aiogram_user = AiogramTgUser(
        id=user_id,
        is_bot=is_bot,
        first_name=first_name,
        username=username
    )

    result_user = await find_or_create_with_update_by_platform_id(session, aiogram_user)

    assert result_user.id == user.id
    assert result_user.bot_status == BotStatusEnum.WORKS
