import random
from unittest.mock import patch

import pytest
from fastapi import status
from models.vacancy import Vacancy
from tests.factories.vacancy import VacancyWithCategoryFactory


@pytest.mark.asyncio
@patch("services.api.vacancy.vacancies_list.get_all_vacancies")
async def test_list_vacancy(mock_get_all_vacancies, client):
    """Тестирует эндпоинт возврата списка всех существующих вакансий"""

    vacancy_count: int = random.randint(4, 10)
    vacancies: list[Vacancy] = [
        VacancyWithCategoryFactory() for _ in range(vacancy_count)
    ]
    mock_get_all_vacancies.return_value = vacancies
    response = await client.get("/vacancies/")

    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == len(vacancies)
