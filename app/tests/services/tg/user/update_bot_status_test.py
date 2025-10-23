from unittest.mock import AsyncMock

import pytest
from enums.bot_status_enum import BotStatusEnum
from models.user import User
from services.tg.user.update_bot_status import update_bot_status
from tests.factories.user import UserFactoryWithoutSubscriptions


@pytest.mark.asyncio
async def test_update_bot_status_bot_blocked():
    """Тестирует обновление статуса бота пользователя."""
    new_user: User = UserFactoryWithoutSubscriptions()

    mock_db = AsyncMock()

    result = await update_bot_status(mock_db, new_user, BotStatusEnum.BOT_BLOCKED)
    assert result.bot_status == BotStatusEnum.BOT_BLOCKED
    mock_db.commit.assert_awaited_once()
    mock_db.refresh.assert_awaited_once_with(new_user)


@pytest.mark.asyncio
async def test_update_bot_status_bot_works():
    """Тестирует обновление статуса бота пользователя."""
    new_user: User = UserFactoryWithoutSubscriptions()

    mock_db = AsyncMock()

    result = await update_bot_status(mock_db, new_user, BotStatusEnum.WORKS)
    assert result.bot_status == BotStatusEnum.WORKS
    mock_db.commit.assert_awaited_once()
    mock_db.refresh.assert_awaited_once_with(new_user)
