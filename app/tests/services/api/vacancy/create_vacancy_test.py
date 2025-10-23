import random
from unittest.mock import AsyncMock

import pytest
from lib.tg.constants import SOURCE
from models.category import Category
from models.vacancy import Vacancy
from schemas.api.vacancies.create.request import CreateVacancyRequest
from services.api.vacancy.create_vacancy import create_vacancy
from tests.factories.category import CategoryFactory


@pytest.mark.asyncio
async def test_create_vacancy():
    """Проверяет создание вакансии"""
    category_name: str = f"Category {random.randint(1, 100)}"
    vacancy_data: dict[str, str] = {
        "title": "Технический специалист",
        "categoryTitle": category_name,
        "description": f"Описание вакансии{random.randint(100, 1000000)}",
        "contactInformation": f"ТГ - @username{random.randint(100, 1000000)}",
        "source": SOURCE,
        "platformId": f"{random.randint(100, 1000000)}",
    }
    create_vacancy_request: CreateVacancyRequest = CreateVacancyRequest(**vacancy_data)
    mock_db = AsyncMock()
    category: Category = CategoryFactory()
    vacancy: Vacancy = await create_vacancy(mock_db, create_vacancy_request, category)

    assert isinstance(vacancy, Vacancy)
    assert vacancy.title == create_vacancy_request.title
    assert vacancy.description == create_vacancy_request.description
    assert vacancy.contact_information == create_vacancy_request.contact_information
    assert vacancy.source == SOURCE
    assert vacancy.platform_id == create_vacancy_request.platform_id
