import random
from unittest.mock import AsyncMock, MagicMock, Mock, patch

import pytest
from enums.bot_status_enum import BotStatusEnum
from services.tg.send_analytics import send_analytics


@pytest.mark.asyncio
# Мокаем саму функцию отправки алерта, так как send_analytics вызывает её
@patch("services.tg.send_analytics.admin_alert_mailing_new_users", new_callable=AsyncMock)
@patch("services.tg.send_analytics.jinja_render", new_callable=AsyncMock)
@patch("services.tg.send_analytics.bot") # Мокаем инстанс бота, который импортируется в файл
async def test_send_analytics(mock_bot, mock_render, mock_admin_alert):
    """
    Тестирует корректность работы функции `send_analytics`.
    """
    # Данные для теста
    jinja_text = "rendered_text"
    user_works_count = random.randint(3, 10)
    user_bot_blocked_count = random.randint(3, 10)
    all_user_count = user_works_count + user_bot_blocked_count

    # Настройка мока базы данных
    mock_db = AsyncMock()

    # Результат первого запроса (group_by)
    mock_result_group = Mock()
    mock_result_group.all.return_value = [
        (BotStatusEnum.WORKS, user_works_count),
        (BotStatusEnum.BOT_BLOCKED, user_bot_blocked_count),
    ]

    # Результат второго запроса (count)
    mock_result_count = Mock()
    mock_result_count.scalar.return_value = all_user_count

    # Последовательные возвраты для db.execute
    mock_db.execute.side_effect = [mock_result_group, mock_result_count]

    # Настройка мока пользователя
    mock_user = MagicMock() # Для моделей лучше MagicMock или Mock, если не нужны await
    mock_user.username = "test_user"

    # Ожидаемая структура данных для рендера
    expected_analytics = {
        BotStatusEnum.WORKS: user_works_count,
        BotStatusEnum.BOT_BLOCKED: user_bot_blocked_count,
        "users_count": all_user_count,
    }

    mock_render.return_value = jinja_text

    # Вызов тестируемой функции
    from services.tg.send_analytics import send_analytics
    await send_analytics(mock_db, mock_user)

    # Проверки
    # 1. Проверяем, что рендер вызван с правильными аргументами
    mock_render.assert_awaited_once_with(
        "analytics",
        {"user": mock_user, "analytics": expected_analytics, "bot_status": BotStatusEnum},
    )

    # 2. Проверяем, что функция алерта вызвана с отрендеренным текстом и моком бота
    mock_admin_alert.assert_awaited_once_with(
        text=jinja_text,
        bot=mock_bot
    )