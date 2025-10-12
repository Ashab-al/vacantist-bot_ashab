import random

import pytest
from models.blacklist import BlackList
from services.api.vacancy.black_list_check import black_list_check
from sqlalchemy.ext.asyncio import AsyncSession
from tests.conftest import create_vacancy_and_category


@pytest.mark.asyncio
async def test_black_list_check_when_vacancy_is_not_blacklist(session):
    """Проверяет нахождение вакансии в черном списке Когда вакансия не находится в черном списке"""
    vacancy, _category = await create_vacancy_and_category(session)

    await black_list_check(session, vacancy.platform_id, vacancy.contact_information)


@pytest.mark.asyncio
async def test_black_list_check_when_vacancy_is_blacklist(session: AsyncSession):
    """Проверяет нахождение вакансии в черном списке Когда вакансия находится в черном списке"""
    vacancy, _category = await create_vacancy_and_category(session)
    complaint_counter: int = random.randint(2, 10)

    with pytest.raises(ValueError, match="Вакансия в черном списке"):
        blacklist: BlackList = BlackList(
            contact_information=vacancy.contact_information,
            complaint_counter=complaint_counter,
        )
        session.add(blacklist)
        await session.commit()
        await session.refresh(blacklist)

        await black_list_check(
            session, vacancy.platform_id, vacancy.contact_information
        )
