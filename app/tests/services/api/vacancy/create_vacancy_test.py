import pytest
from models.category import Category
from models.vacancy import Vacancy
import random
from schemas.api.vacancies.create.request import CreateVacancyRequest
from schemas.api.categories.create import CreateCategoryRequest
from services.api.vacancy.create_vacancy import create_vacancy
from services.api.category.create_category import create_category

from lib.tg.constants import SOURCE

@pytest.mark.asyncio
async def test_create_vacancy(
    session_factory
):
    """Проверяет создание вакансии"""
    category_name: str = f"Category {random.randint(1, 100)}"
    vacancy_data: dict[str, str] = {
        "title": "Технический специалист",
        "categoryTitle": category_name,
        "description": f"Описание вакансии{random.randint(100, 1000000)}",
        "contactInformation": f"ТГ - @username{random.randint(100, 1000000)}",
        "source": SOURCE,
        "platformId": f"{random.randint(100, 1000000)}"
    }
    create_vacancy_request: CreateVacancyRequest = CreateVacancyRequest(**vacancy_data)
    
    async with session_factory() as session:
        category: Category = await create_category(
            session, 
            CreateCategoryRequest(name = category_name)
        )
        vacancy: Vacancy = await create_vacancy(
            session,
            create_vacancy_request,
            category
        )

    assert isinstance(vacancy, Vacancy)
    assert vacancy.title == create_vacancy_request.title
    assert vacancy.description == create_vacancy_request.description
    assert vacancy.contact_information == create_vacancy_request.contact_information
    assert vacancy.source == SOURCE
    assert vacancy.platform_id == create_vacancy_request.platform_id
    
