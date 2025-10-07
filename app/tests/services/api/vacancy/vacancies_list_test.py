import pytest
from lib.tg.constants import SOURCE
from models.blacklist import BlackList
import random
from models.category import Category
from models.vacancy import Vacancy
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.api.categories.create.request import CreateCategoryRequest
from services.api.category.create_category import create_category
from tests.conftest import create_vacancy_and_category
from schemas.api.vacancies.create.request import CreateVacancyRequest
from services.api.vacancy.check_and_create_vacancy import check_and_create_vacancy
from services.api.vacancy.vacancies_list import vacancies_list
from schemas.api.vacancies.vacancy import VacancySchema
from services.api.vacancy.create_vacancy import create_vacancy


@pytest.mark.asyncio
async def test_vacancies_list(
    session_factory: AsyncSession
):
    """Проверяет возврат списка вакансий"""

    count_vacancy = random.randint(3, 10)    
    category_name: str = f"Category {random.randint(1, 100)}"
    
    async with session_factory() as session:
        category: Category = await create_category(
            session, 
            CreateCategoryRequest(name = category_name)
        )
        for i in range(count_vacancy):
            await create_vacancy(
                session,
                category=category,
                vacancy_data=CreateVacancyRequest(
                    title="Технический специалист",
                    category_title=category_name,
                    description=f"Описание вакансии{i}",
                    contact_information=f"ТГ - @username{i}",
                    source=SOURCE,
                    platform_id=f"{i}"  
                )
            )
        
        vacancies: list[VacancySchema] = await vacancies_list(session)

    assert len(vacancies) == count_vacancy
    assert all(isinstance(vacancy, VacancySchema) for vacancy in vacancies)
    
    