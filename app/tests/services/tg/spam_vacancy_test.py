import random

import pytest
from lib.tg.constants import SOURCE
from models.blacklist import BlackList
from schemas.api.categories.create.request import CreateCategoryRequest
from schemas.api.vacancies.create.request import CreateVacancyRequest
from services.api.category.create_category import create_category
from services.api.vacancy.create_vacancy import create_vacancy
from services.tg.vacancy.spam_vacancy import (
    BLACKLISTED,
    COMPLAINT_COUNTER,
    spam_vacancy,
)
from sqlalchemy import select


@pytest.mark.asyncio
async def test_spam_vacancy_creates_blacklist_entry(session):
    """Проверяет, что при первом обращении создаётся запись в BlackList и счётчик = 1"""

    category_name = "IT"
    vacancy_title = "Dev"
    description = "Описание"
    contact_information = "@dev"

    # создаём категорию и вакансию
    category = await create_category(session, CreateCategoryRequest(name=category_name))
    vacancy = await create_vacancy(
        session,
        category=category,
        vacancy_data=CreateVacancyRequest(
            title=vacancy_title,
            category_title=category_name,
            description=description,
            contact_information=contact_information,
            source=SOURCE,
            platform_id=str(random.randint(1, 1000)),
        ),
    )

    result = await spam_vacancy(session, vacancy.id)

    # проверяем, что запись создана
    black_list: BlackList = (
        await session.scalars(
            select(BlackList).filter_by(contact_information=vacancy.platform_id)
        )
    ).one_or_none()

    assert result is None
    assert black_list is not None
    assert black_list.contact_information == vacancy.platform_id
    assert black_list.complaint_counter == 1


@pytest.mark.asyncio
async def test_spam_vacancy_reaches_blacklisted_state(session):
    """Проверяет, что после превышения порога возвращается статус BLACKLISTED"""
    platform_id: str = str(random.randint(1, 1000))
    category_name = "IT"
    vacancy_title = "Dev"
    description = "Описание"
    contact_information = "@dev"

    category = await create_category(session, CreateCategoryRequest(name=category_name))
    vacancy = await create_vacancy(
        session,
        category=category,
        vacancy_data=CreateVacancyRequest(
            title=vacancy_title,
            category_title=category_name,
            description=description,
            contact_information=contact_information,
            source=SOURCE,
            platform_id=platform_id,
        ),
    )

    # создаём запись в BlackList заранее с complaint_counter = порог
    blacklisted = BlackList(
        contact_information=platform_id, complaint_counter=COMPLAINT_COUNTER
    )
    session.add(blacklisted)
    await session.commit()

    result = await spam_vacancy(session, vacancy.id)

    assert result == BLACKLISTED
