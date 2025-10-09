import pytest
from models.blacklist import BlackList
import random
from models.vacancy import Vacancy
from sqlalchemy.ext.asyncio import AsyncSession
from tests.conftest import create_vacancy_and_category
from schemas.api.vacancies.create.request import CreateVacancyRequest
from services.api.vacancy.check_and_create_vacancy import check_and_create_vacancy


@pytest.mark.asyncio
async def test_check_and_create_vacancy_when_vacancy_is_not_blacklist(
    session: AsyncSession
):
    """Проверяет создание вакансии и также проверку вакансии на нахождение в черном списке"""
    vacancy, category = await create_vacancy_and_category(session)
    
    new_vacancy: Vacancy = await check_and_create_vacancy(
        session,
        CreateVacancyRequest(
            title=vacancy.title,
            category_title=category.name,
            description=vacancy.description,
            contact_information=vacancy.contact_information,
            source=vacancy.source,
            platform_id=vacancy.platform_id
        )    
    )

    assert isinstance(new_vacancy, Vacancy)
    
    
@pytest.mark.asyncio
async def test_check_and_create_vacancy_when_vacancy_is_blacklist(
    session: AsyncSession
):
    """
    Проверяет создание вакансии и также проверку вакансии на нахождение в черном списке
    Когда вакансия находится в черном списке
    """
    vacancy, category = await create_vacancy_and_category(session)
    complaint_counter: int = random.randint(3, 10)
    
    with pytest.raises(
        ValueError, 
        match='Вакансия в черном списке'
    ):
        blacklist: BlackList = BlackList(
            contact_information=vacancy.contact_information,
            complaint_counter=complaint_counter
        )
        session.add(blacklist)
        await session.commit()
        await session.refresh(blacklist)
        
        await check_and_create_vacancy(
            session,
            CreateVacancyRequest(
                title=vacancy.title,
                category_title=category.name,
                description=vacancy.description,
                contact_information=vacancy.contact_information,
                source=vacancy.source,
                platform_id=vacancy.platform_id
            )    
        )

@pytest.mark.asyncio
async def test_check_and_create_vacancy_when_category_is_not_exist(
    session: AsyncSession
):
    """
    Проверяет создание вакансии и также проверку вакансии на нахождение в черном списке
    Когда категория не существует
    """
    vacancy, _category = await create_vacancy_and_category(session)
    new_category_name = f"Категория {random.randint(1, 1000)}"

    with pytest.raises(
        ValueError, 
        match='Такой категории не существует'
    ):
        await check_and_create_vacancy(
            session,
            CreateVacancyRequest(
                title=vacancy.title,
                category_title=new_category_name,
                description=vacancy.description,
                contact_information=vacancy.contact_information,
                source=vacancy.source,
                platform_id=vacancy.platform_id
            )    
        )