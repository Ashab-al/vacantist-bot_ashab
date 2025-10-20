import random
from math import ceil
from unittest.mock import AsyncMock, patch

import pytest
from bot.keyboards.get_vacancies_button import PAGE, PAGE_SIZE
from enums.vacancies_for_the_week_enum import VacanciesForTheWeekStatusEnum
from models.category import Category
from models.user import User
from models.vacancy import Vacancy
from services.tg.vacancy.vacancies_for_the_week import fetch_vacancies_for_the_week
from tests.factories.category import CategoryFactory
from tests.factories.user import UserFactoryWithoutSubscriptions
from tests.factories.vacancy import VacancyWithCategoryFactory


@pytest.mark.asyncio
@patch("services.tg.vacancy.vacancies_for_the_week.VacancyForTheWeekQuery")
@patch("services.tg.vacancy.vacancies_for_the_week.find_subscribe")
async def test_vacancies_for_the_week(mock_find_subscribe, mock_vacancy_query):
    """
    Проверяет пагинацию когда есть подписки на категории и когда есть вакансии у этих категорий
    """
    random_count_categories: int = random.randint(3, 10)

    new_user: User = UserFactoryWithoutSubscriptions()
    mock_db = AsyncMock()

    vacancies: list[Vacancy] = [
        VacancyWithCategoryFactory() for _ in range(random_count_categories)
    ]
    categories: list[Category] = [vacancy.category for vacancy in vacancies]

    new_user.categories.extend(categories)
    mock_find_subscribe.return_value = new_user.categories
    mock_query_instance = AsyncMock()
    mock_vacancy_query.return_value = mock_query_instance
    mock_query_instance.build_vacancies_for_the_week.return_value = vacancies[
        0:PAGE_SIZE
    ]
    mock_query_instance.total_count.return_value = len(vacancies)

    result = await fetch_vacancies_for_the_week(mock_db, new_user, PAGE, PAGE_SIZE)

    assert result.get("status") == VacanciesForTheWeekStatusEnum.OK
    assert len(result.get("items")) == PAGE_SIZE
    assert result.get("meta").get("count") == len(vacancies)
    assert result.get("meta").get("page") == PAGE
    assert result.get("meta").get("max_pages") == ceil(len(categories) / PAGE_SIZE)
    mock_find_subscribe.assert_awaited_once_with(mock_db, new_user)
    mock_vacancy_query.assert_called_once_with(mock_db, new_user, PAGE, PAGE_SIZE)
    mock_query_instance.build_vacancies_for_the_week.assert_awaited_once_with(
        new_user.categories
    )
    mock_query_instance.total_count.assert_awaited_once()


@pytest.mark.asyncio
@patch("services.tg.vacancy.vacancies_for_the_week.VacancyForTheWeekQuery")
@patch("services.tg.vacancy.vacancies_for_the_week.find_subscribe")
async def test_vacancies_for_the_week_when_has_not_subscribes(
    mock_find_subscribe, mock_vacancy_query
):
    """Проверяет пагинацию когда нет подписок на категории"""
    new_user: User = UserFactoryWithoutSubscriptions()
    mock_db = AsyncMock()

    find_vacancies = []
    subscribe_categories: list = []
    mock_find_subscribe.return_value = subscribe_categories
    mock_query_instance = AsyncMock()
    mock_vacancy_query.return_value = mock_query_instance
    mock_query_instance.build_vacancies_for_the_week.return_value = find_vacancies
    mock_query_instance.total_count.return_value = len(find_vacancies)
    result = await fetch_vacancies_for_the_week(mock_db, new_user, PAGE, PAGE_SIZE)

    assert (
        result.get("status")
        == VacanciesForTheWeekStatusEnum.SUBSCRIBED_CATEGORIES_EMPTY
    )
    mock_find_subscribe.assert_awaited_once_with(mock_db, new_user)
    mock_query_instance.build_vacancies_for_the_week.assert_not_awaited()
    mock_query_instance.total_count.assert_not_awaited()


@pytest.mark.asyncio
@patch("services.tg.vacancy.vacancies_for_the_week.VacancyForTheWeekQuery")
@patch("services.tg.vacancy.vacancies_for_the_week.find_subscribe")
async def test_vacancies_for_the_week_when_has_subscribes_but_has_not_vacancies(
    mock_find_subscribe, mock_vacancy_query
):
    """Проверяет пагинацию когда есть подписки на категории но нет вакансий"""
    random_count_categories: int = random.randint(3, 10)

    new_user: User = UserFactoryWithoutSubscriptions()
    mock_db = AsyncMock()

    categories: list[Vacancy] = [
        CategoryFactory() for _ in range(random_count_categories)
    ]
    vacancies: list = []
    new_user.categories.extend(categories)
    mock_find_subscribe.return_value = new_user.categories
    mock_query_instance = AsyncMock()
    mock_vacancy_query.return_value = mock_query_instance
    mock_query_instance.build_vacancies_for_the_week.return_value = vacancies
    mock_query_instance.total_count.return_value = len(vacancies)

    result = await fetch_vacancies_for_the_week(mock_db, new_user, PAGE, PAGE_SIZE)

    assert result.get("status") == VacanciesForTheWeekStatusEnum.VACANCY_LIST_EMPTY
    mock_find_subscribe.assert_awaited_once_with(mock_db, new_user)
    mock_vacancy_query.assert_called_once_with(mock_db, new_user, PAGE, PAGE_SIZE)
    mock_query_instance.build_vacancies_for_the_week.assert_awaited_once_with(
        new_user.categories
    )
    mock_query_instance.total_count.assert_not_awaited()
