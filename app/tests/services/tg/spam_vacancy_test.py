from unittest.mock import AsyncMock, patch

import pytest
from models.blacklist import BlackList
from models.vacancy import Vacancy
from services.tg.vacancy.spam_vacancy import (
    BLACKLISTED,
    COMPLAINT_COUNTER,
    spam_vacancy,
)
from tests.factories.vacancy import VacancyWithCategoryFactory


@pytest.mark.asyncio
@patch("services.tg.vacancy.spam_vacancy.find_vacancy_by_id")
@patch(
    "services.tg.vacancy.spam_vacancy.black_list_check_by_platform_id_or_contact_information",
)
async def test_spam_vacancy_creates_blacklist_entry(
    mock_black_list_check_by_platform_id_or_contact_information,
    mock_find_vacancy_by_id,
):
    """Проверяет, что при первом обращении создаётся запись в BlackList"""
    vacancy: Vacancy = VacancyWithCategoryFactory()
    mock_find_vacancy_by_id.return_value = vacancy
    mock_black_list_check_by_platform_id_or_contact_information.return_value = None
    mock_db = AsyncMock()

    result = await spam_vacancy(mock_db, vacancy.id)

    mock_black_list_check_by_platform_id_or_contact_information.assert_awaited_once_with(
        mock_db, contact_information=vacancy.platform_id
    )
    assert result is None


@pytest.mark.asyncio
@patch("services.tg.vacancy.spam_vacancy.find_vacancy_by_id")
@patch(
    "services.tg.vacancy.spam_vacancy.black_list_check_by_platform_id_or_contact_information",
)
async def test_spam_vacancy_reaches_blacklisted_state(
    mock_black_list_check_by_platform_id_or_contact_information,
    mock_find_vacancy_by_id,
):
    """Проверяет, что после превышения порога возвращается статус BLACKLISTED"""
    mock_db = AsyncMock()
    vacancy: Vacancy = VacancyWithCategoryFactory()
    blacklisted = BlackList(
        contact_information=vacancy.platform_id, complaint_counter=COMPLAINT_COUNTER
    )
    mock_find_vacancy_by_id.return_value = vacancy
    mock_black_list_check_by_platform_id_or_contact_information.return_value = (
        blacklisted
    )

    result = await spam_vacancy(mock_db, vacancy.id)

    assert result == BLACKLISTED
