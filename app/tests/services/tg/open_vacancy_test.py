import random
import pytest
from models.blacklist import BlackList
from models.user import User
from services.tg.spam_vacancy import COMPLAINT_COUNTER
from services.tg.open_vacancy import open_vacancy, ZERO_BALANCE
from enums.check_vacancy_enum import CheckVacancyEnum
from tests.conftest import (
    create_tg_user_with_session,
    create_vacancy_and_category_with_session,
)


@pytest.mark.asyncio
async def test_open_vacancy(session):
    """Проверяет открытие вакансии"""
    vacancy, _category = await create_vacancy_and_category_with_session(session)
    user: User = await create_tg_user_with_session(session)
    result_open_vacancy: dict = await open_vacancy(session, user, vacancy.id)

    assert result_open_vacancy.get("status") == CheckVacancyEnum.OPEN_VACANCY
    assert result_open_vacancy.get("vacancy") == vacancy
    assert result_open_vacancy.get("path_view") in "callback_query/open_vacancy"
    assert result_open_vacancy.get("low_points") == True


@pytest.mark.asyncio
async def test_open_vacancy_when_vacancy_is_not_exist(session):
    """Проверяет открытие вакансии когда вакансии не существует"""
    vacancy_id: int = random.randint(1, 1000)

    with pytest.raises(
        ValueError, match=f"{vacancy_id} - такой вакансии нет в базе данных"
    ):
        user: User = await create_tg_user_with_session(session)

        await open_vacancy(session, user, vacancy_id)


@pytest.mark.asyncio
async def test_open_vacancy_when_user_balance_zero(session):
    """Проверяет открытие вакансии когда баланс пользователя нулевой"""
    vacancy, _category = await create_vacancy_and_category_with_session(session)
    user: User = await create_tg_user_with_session(session)
    user.bonus = ZERO_BALANCE
    user.point = ZERO_BALANCE

    session.add(user)
    await session.commit()
    await session.refresh(user)

    result_open_vacancy: dict = await open_vacancy(session, user, vacancy.id)

    assert result_open_vacancy.get("status") == CheckVacancyEnum.WARNING
    assert result_open_vacancy.get("path_view") in "callback_query/out_of_points"


@pytest.mark.asyncio
async def test_open_vacancy_when_vacancy_in_blacklist(session):
    """Проверяет открытие вакансии когда вакансия находится в черном списке"""
    vacancy, _category = await create_vacancy_and_category_with_session(session)
    user: User = await create_tg_user_with_session(session)

    blacklisted = BlackList(
        contact_information=vacancy.platform_id, complaint_counter=COMPLAINT_COUNTER
    )

    session.add(blacklisted)
    await session.commit()

    result_open_vacancy: dict = await open_vacancy(session, user, vacancy.id)
    assert result_open_vacancy.get("status") == CheckVacancyEnum.WARNING
    assert result_open_vacancy.get("vacancy") == vacancy
    assert result_open_vacancy.get("path_view") in "callback_query/add_to_blacklist"
