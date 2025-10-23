import random
from unittest.mock import AsyncMock, patch

import pytest
from models.vacancy import Vacancy
from schemas.api.vacancies.vacancy import VacancySchema
from services.api.vacancy.vacancies_list import vacancies_list
from tests.factories.vacancy import VacancyWithCategoryFactory


@pytest.mark.asyncio
@patch("services.api.vacancy.vacancies_list.get_all_vacancies")
async def test_vacancies_list(mock_get_all_vacancies):
    """Проверяет возврат списка вакансий"""

    count_vacancy = random.randint(3, 10)
    mock_db = AsyncMock()

    vacancies: list[Vacancy] = [
        VacancyWithCategoryFactory() for _ in range(count_vacancy)
    ]

    mock_get_all_vacancies.return_value = vacancies

    vacancies: list[VacancySchema] = await vacancies_list(mock_db)

    mock_get_all_vacancies.assert_awaited_once_with(mock_db)
    assert len(vacancies) == count_vacancy
    assert all(isinstance(vacancy, VacancySchema) for vacancy in vacancies)
