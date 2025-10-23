import random
from unittest.mock import AsyncMock, patch

import pytest
from exceptions.category.category_not_found_error import CategoryNotFoundError
from exceptions.vacancy.blacklisted_vacancy import BlacklistedVacancyError
from models.blacklist import BlackList
from models.category import Category
from models.vacancy import Vacancy
from schemas.api.vacancies.create.request import CreateVacancyRequest
from services.api.vacancy.check_and_create_vacancy import check_and_create_vacancy
from tests.factories.vacancy import VacancyWithCategoryFactory


@pytest.mark.asyncio
@patch("services.api.vacancy.check_and_create_vacancy.get_category_by_name")
@patch("services.api.vacancy.check_and_create_vacancy.black_list_check")
async def test_check_and_create_vacancy_when_vacancy_is_not_blacklist(
    mock_black_list_check, mock_get_category_by_name
):
    """Проверяет создание вакансии и также проверку вакансии на нахождение в черном списке"""
    vacancy: Vacancy = VacancyWithCategoryFactory()
    category: Category = vacancy.category
    mock_db = AsyncMock()
    mock_black_list_check.return_value = None
    mock_get_category_by_name.return_value = category

    new_vacancy: Vacancy = await check_and_create_vacancy(
        mock_db,
        CreateVacancyRequest(
            title=vacancy.title,
            category_title=category.name,
            description=vacancy.description,
            contact_information=vacancy.contact_information,
            source=vacancy.source,
            platform_id=vacancy.platform_id,
        ),
    )

    assert isinstance(new_vacancy, Vacancy)


@pytest.mark.asyncio
@patch(
    "services.api.vacancy.black_list_check.black_list_check_by_platform_id_or_contact_information"
)
@patch("services.api.vacancy.check_and_create_vacancy.get_category_by_name")
async def test_check_and_create_vacancy_when_vacancy_is_blacklist(
    mock_get_category_by_name,
    mock_black_list_check_by_platform_id_or_contact_information,
):
    """
    Проверяет создание вакансии и также проверку вакансии на нахождение в черном списке
    Когда вакансия находится в черном списке
    """
    mock_db = AsyncMock()
    vacancy: Vacancy = VacancyWithCategoryFactory()
    category: Category = vacancy.category
    complaint_counter: int = random.randint(3, 10)
    blacklist: BlackList = BlackList(
        contact_information=vacancy.contact_information,
        complaint_counter=complaint_counter,
    )
    mock_black_list_check_by_platform_id_or_contact_information.return_value = blacklist
    mock_get_category_by_name.return_value = category
    with pytest.raises(BlacklistedVacancyError):
        await check_and_create_vacancy(
            mock_db,
            CreateVacancyRequest(
                title=vacancy.title,
                category_title=category.name,
                description=vacancy.description,
                contact_information=vacancy.contact_information,
                source=vacancy.source,
                platform_id=vacancy.platform_id,
            ),
        )


@pytest.mark.asyncio
@patch("services.api.vacancy.check_and_create_vacancy.get_category_by_name")
@patch("services.api.vacancy.check_and_create_vacancy.black_list_check")
async def test_check_and_create_vacancy_when_category_is_not_exist(
    mock_black_list_check, mock_get_category_by_name
):
    """
    Проверяет создание вакансии и также проверку вакансии на нахождение в черном списке
    Когда категория не существует
    """
    vacancy: Vacancy = VacancyWithCategoryFactory()
    mock_db = AsyncMock()
    new_category_name = f"Категория {random.randint(1, 1000)}"
    mock_black_list_check.return_value = None
    mock_get_category_by_name.return_value = None
    with pytest.raises(CategoryNotFoundError):
        await check_and_create_vacancy(
            mock_db,
            CreateVacancyRequest(
                title=vacancy.title,
                category_title=new_category_name,
                description=vacancy.description,
                contact_information=vacancy.contact_information,
                source=vacancy.source,
                platform_id=vacancy.platform_id,
            ),
        )
