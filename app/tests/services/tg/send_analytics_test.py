import random
from unittest.mock import AsyncMock, Mock, patch

import pytest
from enums.bot_status_enum import BotStatusEnum
from models.user import User
from services.tg.send_analytics import send_analytics, settings
from sqlalchemy.ext.asyncio import AsyncSession


@pytest.mark.asyncio
async def test_send_analytics():
    """
    Тестирует корректность работы функции `send_analytics`.

    Основная цель:
    - Проверить, что аналитика пользователей формируется верно.
    - Убедиться, что шаблон рендерится с правильными данными.
    - Проверить вызов метода отправки сообщения в админский чат.

    Используемые моки:
    - База данных (`AsyncMock`) имитирует запросы к реальной БД.
    - `jinja_render` и `bot.send_message` заменены на асинхронные моки для изоляции теста.

    Проверяемые условия:
    1. Корректное группирование пользователей по статусам.
    2. Рендер шаблона с правильным контекстом.
    3. Вызов `bot.send_message` с текстом сообщения и ID чата.
    """
    jinja_text: str = "rendered_text"
    user_works_count: int = random.randint(3, 10)
    user_bot_blocked_count: int = random.randint(3, 10)
    all_user_count = user_works_count + user_bot_blocked_count
    username: str = "test_user"
    mock_db = AsyncMock(spec=AsyncSession)

    mock_result_group = Mock()
    mock_result_group.all.return_value = [
        (BotStatusEnum.WORKS, user_works_count),
        (BotStatusEnum.BOT_BLOCKED, user_bot_blocked_count),
    ]

    mock_result_count = Mock()
    mock_result_count.scalar.return_value = all_user_count

    mock_db.execute.side_effect = [mock_result_group, mock_result_count]

    mock_user = AsyncMock(spec=User)
    mock_user.username = username

    # Мок jinja_render и bot.send_message
    with patch(
        "services.tg.send_analytics.jinja_render", new_callable=AsyncMock
    ) as mock_render, patch(
        "services.tg.send_analytics.bot.send_message", new_callable=AsyncMock
    ) as mock_send:

        mock_render.return_value = jinja_text

        await send_analytics(mock_db, mock_user)

        mock_render.assert_awaited_once_with(
            "analytics",
            {
                "user": mock_user,
                "analytics": {
                    BotStatusEnum.WORKS: user_works_count,
                    BotStatusEnum.BOT_BLOCKED: user_bot_blocked_count,
                    "users_count": all_user_count,
                },
                "bot_status": BotStatusEnum,
            },
        )

        # Проверяем вызов bot.send_message
        mock_send.assert_awaited_once_with(
            chat_id=settings.admin_chat_id, text=jinja_text
        )
