from unittest.mock import AsyncMock, patch

import pytest
from enums.check_vacancy_enum import CheckVacancyEnum
from services.tg.vacancy.open_vacancy import POINTS_EDGE
from services.tg.vacancy.open_vacancy_and_show_alert import open_vacancy_and_show_alert
from tests.factories.user import UserFactoryWithoutSubscriptions
from tests.factories.vacancy import VacancyWithCategoryFactory


@pytest.mark.asyncio
@patch("services.tg.vacancy.open_vacancy_and_show_alert.open_vacancy")
@patch("services.tg.vacancy.open_vacancy_and_show_alert.find_user_by_platform_id")
async def test_open_vacancy_and_show_alert(
    mock_find_user_by_platform_id, mock_open_vacancy
):
    """Проверяет открытие вакансии и показ алерта при необходимости"""
    mock_db = AsyncMock()
    user = UserFactoryWithoutSubscriptions()
    vacancy = VacancyWithCategoryFactory()
    mock_find_user_by_platform_id.return_value = user
    mock_open_vacancy.return_value = {
        "status": CheckVacancyEnum.OPEN_VACANCY,
        "vacancy": vacancy,
        "path_view": "callback_query/open_vacancy",
        "low_points": user.point <= POINTS_EDGE,
    }
    callback = AsyncMock()
    callback_data = AsyncMock()
    result = await open_vacancy_and_show_alert(callback, callback_data, mock_db)

    callback.answer.assert_awaited_once()
    mock_find_user_by_platform_id.assert_awaited_once_with(
        mock_db, callback.from_user.id
    )
    mock_open_vacancy.assert_awaited_once_with(mock_db, user, callback_data.vacancy_id)
    assert result[0]["status"] == CheckVacancyEnum.OPEN_VACANCY
    assert result[1] == user
