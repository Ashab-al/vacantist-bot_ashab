import random
from unittest.mock import AsyncMock, patch

import pytest
from exceptions.vacancy.blacklisted_vacancy import BlacklistedVacancyError
from models.blacklist import BlackList
from models.vacancy import Vacancy
from services.api.vacancy.black_list_check import black_list_check
from tests.factories.vacancy import VacancyWithCategoryFactory


@pytest.mark.asyncio
@patch(
    "services.api.vacancy.black_list_check.black_list_check_by_platform_id_or_contact_information"
)
async def test_black_list_check_when_vacancy_is_not_blacklist(
    mock_black_list_check_by_platform_id_or_contact_information,
):
    """Проверяет нахождение вакансии в черном списке Когда вакансия не находится в черном списке"""
    mock_db = AsyncMock()
    vacancy: Vacancy = VacancyWithCategoryFactory()
    mock_black_list_check_by_platform_id_or_contact_information.return_value = None

    await black_list_check(mock_db, vacancy.platform_id, vacancy.contact_information)
    mock_black_list_check_by_platform_id_or_contact_information.assert_awaited_once_with(
        mock_db,
        platform_id=vacancy.platform_id,
        contact_information=vacancy.contact_information,
    )


@pytest.mark.asyncio
@patch(
    "services.api.vacancy.black_list_check.black_list_check_by_platform_id_or_contact_information"
)
async def test_black_list_check_when_vacancy_is_blacklist(
    mock_black_list_check_by_platform_id_or_contact_information,
):
    """Проверяет нахождение вакансии в черном списке Когда вакансия находится в черном списке"""
    vacancy: Vacancy = VacancyWithCategoryFactory()
    complaint_counter: int = random.randint(2, 10)
    blacklist: BlackList = BlackList(
        contact_information=vacancy.contact_information,
        complaint_counter=complaint_counter,
    )
    mock_black_list_check_by_platform_id_or_contact_information.return_value = blacklist
    mock_db = AsyncMock()
    with pytest.raises(BlacklistedVacancyError):
        await black_list_check(
            mock_db, vacancy.platform_id, vacancy.contact_information
        )
