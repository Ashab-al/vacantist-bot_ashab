from unittest.mock import patch

import pytest
from fastapi import status
from models.vacancy import Vacancy
from tests.factories.vacancy import VacancyWithCategoryFactory


@pytest.mark.asyncio
@patch("api.vacancies.create.CreateVacancyResponse")
@patch("services.api.vacancy.check_and_create_vacancy.get_category_by_name")
@patch("services.api.vacancy.check_and_create_vacancy.black_list_check")
@patch("api.vacancies.create.add_vacancy_to_sending_queue")
async def test_create_vacancy(
    mock_add_vacancy_to_sending_queue,
    mock_black_list_check,
    mock_get_category_by_name,
    mock_create_vacancy_response,
    client,
):
    """Проверяет создание вакансии"""
    vacancy: Vacancy = VacancyWithCategoryFactory()
    vacancy_data: dict[str, str] = {
        "title": vacancy.title,
        "categoryTitle": vacancy.category.name,
        "description": vacancy.description,
        "contactInformation": vacancy.contact_information,
        "source": vacancy.source,
        "platformId": vacancy.platform_id,
    }

    mock_add_vacancy_to_sending_queue.return_value = None
    mock_black_list_check.return_value = None
    mock_get_category_by_name.return_value = vacancy.category
    mock_create_vacancy_response.return_value = True

    response = await client.post("/vacancies/", json=vacancy_data)
    mock_add_vacancy_to_sending_queue.assert_awaited_once()
    called_arg = mock_add_vacancy_to_sending_queue.await_args.args[0]

    assert isinstance(called_arg, Vacancy)
    assert response.status_code == status.HTTP_200_OK
