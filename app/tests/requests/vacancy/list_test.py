import random

import pytest
from models.vacancy import Vacancy
from tests.conftest import create_vacancy_and_category


@pytest.mark.asyncio
async def test_list_vacancy(client, session):
    """Тестирует эндпоинт возврата списка всех существующих вакансий"""

    vacancy_count: int = random.randint(4, 10)
    vacancies: list[Vacancy] = []

    for _ in range(vacancy_count):
        vacancy, _category = await create_vacancy_and_category(session)
        vacancies.append(vacancy)

    response = await client.get("/vacancies/")

    assert response.status_code == 200
    assert len(response.json()) == len(vacancies)
