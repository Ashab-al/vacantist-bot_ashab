import random
from unittest.mock import AsyncMock, Mock, patch

import pytest
from enums.bot_status_enum import BotStatusEnum
from services.tg.send_analytics import send_analytics, settings


@pytest.mark.asyncio
@patch("services.tg.send_analytics.bot.send_message")
@patch("services.tg.send_analytics.jinja_render")
async def test_send_analytics(mock_render, mock_send):
    """
    Тестирует корректность работы функции `send_analytics`.
    """
    jinja_text: str = "rendered_text"
    user_works_count: int = random.randint(3, 10)
    user_bot_blocked_count: int = random.randint(3, 10)
    all_user_count = user_works_count + user_bot_blocked_count
    username: str = "test_user"

    mock_db = AsyncMock()

    mock_result_group = Mock()
    mock_result_group.all.return_value = [
        (BotStatusEnum.WORKS, user_works_count),
        (BotStatusEnum.BOT_BLOCKED, user_bot_blocked_count),
    ]

    mock_result_count = Mock()
    mock_result_count.scalar.return_value = all_user_count

    mock_db.execute.side_effect = [mock_result_group, mock_result_count]

    mock_user = AsyncMock()
    mock_user.username = username
    render_data = {
        "user": mock_user,
        "analytics": {
            BotStatusEnum.WORKS: user_works_count,
            BotStatusEnum.BOT_BLOCKED: user_bot_blocked_count,
            "users_count": all_user_count,
        },
        "bot_status": BotStatusEnum,
    }
    mock_render.return_value = jinja_text

    await send_analytics(mock_db, mock_user)

    mock_render.assert_awaited_once_with("analytics", render_data)

    mock_send.assert_awaited_once_with(chat_id=settings.admin_chat_id, text=jinja_text)
