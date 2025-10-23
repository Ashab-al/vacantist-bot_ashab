import random
from unittest.mock import AsyncMock, patch

import pytest
from enums.check_vacancy_enum import CheckVacancyEnum
from models.user import User
from services.tg.vacancy.open_vacancy import open_vacancy
from tests.factories.user import UserFactoryWithoutSubscriptions
from tests.factories.vacancy import VacancyWithCategoryFactory


@pytest.mark.asyncio
@patch("services.tg.vacancy.open_vacancy._check_blacklist")
@patch("services.tg.vacancy.open_vacancy.find_vacancy_by_id")
async def test_open_vacancy(mock_find_vacancy_by_id, mock_check_blacklist):
    """Проверяет открытие вакансии"""
    user_point_count: int = 3
    vacancy = VacancyWithCategoryFactory()
    user: User = UserFactoryWithoutSubscriptions()
    user.point = user_point_count
    mock_db = AsyncMock()
    mock_find_vacancy_by_id.return_value = vacancy
    mock_check_blacklist.return_value = False

    result_open_vacancy: dict = await open_vacancy(mock_db, user, vacancy.id)

    assert result_open_vacancy.get("status") == CheckVacancyEnum.OPEN_VACANCY
    assert result_open_vacancy.get("vacancy") == vacancy
    assert result_open_vacancy.get("path_view") in "callback_query/open_vacancy"
    assert result_open_vacancy.get("low_points") is True


@pytest.mark.asyncio
@patch("services.tg.vacancy.open_vacancy.find_vacancy_by_id")
async def test_open_vacancy_when_vacancy_is_not_exist(mock_find_vacancy_by_id):
    """Проверяет открытие вакансии когда вакансии не существует"""
    mock_find_vacancy_by_id.return_value = None
    vacancy_id: int = random.randint(1, 1000)
    mock_db = AsyncMock()
    user: User = UserFactoryWithoutSubscriptions()
    with pytest.raises(
        ValueError, match=f"{vacancy_id} - такой вакансии нет в базе данных"
    ):
        await open_vacancy(mock_db, user, vacancy_id)


@pytest.mark.asyncio
@patch("services.tg.vacancy.open_vacancy._check_blacklist")
@patch("services.tg.vacancy.open_vacancy.find_vacancy_by_id")
async def test_open_vacancy_when_user_balance_zero(
    mock_find_vacancy_by_id, mock_check_blacklist
):
    """Проверяет открытие вакансии когда баланс пользователя нулевой"""
    vacancy = VacancyWithCategoryFactory()
    user: User = UserFactoryWithoutSubscriptions()
    mock_db = AsyncMock()
    mock_find_vacancy_by_id.return_value = vacancy
    mock_check_blacklist.return_value = False

    result_open_vacancy: dict = await open_vacancy(mock_db, user, vacancy.id)

    assert result_open_vacancy.get("status") == CheckVacancyEnum.WARNING
    assert result_open_vacancy.get("path_view") in "callback_query/out_of_points"


@pytest.mark.asyncio
@patch("services.tg.vacancy.open_vacancy._check_blacklist")
@patch("services.tg.vacancy.open_vacancy.find_vacancy_by_id")
async def test_open_vacancy_when_vacancy_in_blacklist(
    mock_find_vacancy_by_id, mock_check_blacklist
):
    """Проверяет открытие вакансии когда вакансия находится в черном списке"""
    user_point_count: int = 3
    vacancy = VacancyWithCategoryFactory()
    user: User = UserFactoryWithoutSubscriptions()
    user.point = user_point_count
    mock_db = AsyncMock()
    mock_find_vacancy_by_id.return_value = vacancy
    mock_check_blacklist.return_value = True

    result_open_vacancy: dict = await open_vacancy(mock_db, user, vacancy.id)
    assert result_open_vacancy.get("status") == CheckVacancyEnum.WARNING
    assert result_open_vacancy.get("vacancy") == vacancy
    assert result_open_vacancy.get("path_view") in "callback_query/add_to_blacklist"
