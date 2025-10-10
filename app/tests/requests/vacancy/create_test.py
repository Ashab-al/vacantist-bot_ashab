import random
import pytest
from lib.tg.constants import SOURCE
from models.category import Category
from models.vacancy import Vacancy
from schemas.api.categories.create import CreateCategoryRequest
from services.api.category.create_category import create_category


@pytest.mark.asyncio
async def test_create_vacancy(client, session, mocker):
    """Проверяет создание вакансии"""
    category_name: str = f"Category {random.randint(1, 10000000000)}"
    description: str = f"Описание вакансии{random.randint(100, 1000000)}"
    contact_information: str = f"ТГ - @username{random.randint(100, 1000000)}"
    platform_id: str = f"{random.randint(100, 1000000)}"

    vacancy_data: dict[str, str] = {
        "title": category_name,
        "categoryTitle": category_name,
        "description": description,
        "contactInformation": contact_information,
        "source": SOURCE,
        "platformId": platform_id,
    }
    _category: Category = await create_category(
        session, CreateCategoryRequest(name=category_name)
    )
    mock_add_vacancy_to_sending_queue = mocker.patch(
        "api.vacancies.create.add_vacancy_to_sending_queue"
    )

    response = await client.post("/vacancies/", json=vacancy_data)
    mock_add_vacancy_to_sending_queue.assert_awaited_once()
    called_arg = mock_add_vacancy_to_sending_queue.await_args.args[0]

    assert isinstance(called_arg, Vacancy)
    assert response.status_code == 200
    assert response.json().get("title") == category_name
    assert response.json().get("description") == description
    assert response.json().get("contactInformation") == contact_information
    assert response.json().get("source") == SOURCE
    assert response.json().get("platformId") == platform_id
