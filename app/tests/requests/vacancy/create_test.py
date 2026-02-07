from unittest.mock import AsyncMock, patch

import pytest
from fastapi import status
from models.vacancy import Vacancy
from tests.factories.vacancy import VacancyWithCategoryFactory


@pytest.mark.asyncio
async def test_create_vacancy(client):
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

    with patch(
        "api.vacancies.create.check_and_create_vacancy",
        new_callable=AsyncMock,
        return_value=vacancy,
    ), patch(
        "api.vacancies.create.sender_vacancy",
        new_callable=AsyncMock,
    ) as mock_sender:
        response = await client.post("/vacancies/", json=vacancy_data)

        assert response.status_code == status.HTTP_200_OK
        assert response.json()["id"] == vacancy.id
        assert response.json()["title"] == vacancy.title
        mock_sender.assert_called_once_with(vacancy.id)


@pytest.mark.asyncio
async def test_create_vacancy_blacklisted(client):
    """Проверяет создание вакансии из черного списка"""
    from exceptions.vacancy.blacklisted_vacancy import BlacklistedVacancyError

    vacancy_data: dict[str, str] = {
        "title": "Test",
        "categoryTitle": "Test",
        "description": "Test",
        "contactInformation": "Test",
        "source": "Test",
        "platformId": "123",
    }

    with patch(
        "api.vacancies.create.check_and_create_vacancy",
        new_callable=AsyncMock,
        side_effect=BlacklistedVacancyError(),
    ):
        response = await client.post("/vacancies/", json=vacancy_data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST