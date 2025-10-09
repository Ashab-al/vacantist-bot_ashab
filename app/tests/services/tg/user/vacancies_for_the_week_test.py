import pytest
import random
from enums.vacancies_for_the_week_enum import VacanciesForTheWeekStatusEnum
from models.category import Category
from models.user import User
from repositories.users.get_user_by_id import get_user_by_id
from schemas.api.categories.create.request import CreateCategoryRequest
from services.api.category.create_category import create_category
from services.tg.vacancy.vacancies_for_the_week import fetch_vacancies_for_the_week
from tests.conftest import create_tg_user_with_session, create_vacancy_and_category_with_session
from bot.keyboards.get_vacancies_button import PAGE, PAGE_SIZE
from math import ceil


@pytest.mark.asyncio
async def test_vacancies_for_the_week(
    session
):
    """Проверяет пагинацию когда есть подписки на категории и когда есть вакансии у этих категорий"""
    subscribe_count: int = random.randint(3, 10)
    categories = []
    vacancies = []
    for _ in range(subscribe_count):
        vacancy, category = await create_vacancy_and_category_with_session(session)
        categories.append(category)
        vacancies.append(vacancy)
    user: User = await get_user_by_id(
        session, 
        user_id=(await create_tg_user_with_session(session)).id
    )
    user.categories.extend(categories)
    await session.commit()

    result = await fetch_vacancies_for_the_week(
        session,
        user,
        PAGE,
        PAGE_SIZE
    )
        

    assert result.get('status') == VacanciesForTheWeekStatusEnum.OK
    assert len(result.get('items')) == PAGE_SIZE
    assert result.get('meta').get('count') == len(vacancies)
    assert result.get('meta').get('page') == PAGE
    assert result.get('meta').get('max_pages') == ceil(len(categories) / PAGE_SIZE)
        
    
@pytest.mark.asyncio
async def test_vacancies_for_the_week_when_has_not_subscribes(
    session
):
    """Проверяет пагинацию когда нет подписок на категории"""
    subscribe_count: int = random.randint(3, 10)

    for _ in range(subscribe_count):
        _vacancy, _category = await create_vacancy_and_category_with_session(session)

    user: User = await get_user_by_id(
        session, 
        user_id=(await create_tg_user_with_session(session)).id
    )
    
    result = await fetch_vacancies_for_the_week(
        session,
        user,
        PAGE,
        PAGE_SIZE
    )
        
    assert result.get('status') == VacanciesForTheWeekStatusEnum.SUBSCRIBED_CATEGORIES_EMPTY


@pytest.mark.asyncio
async def test_vacancies_for_the_week_when_has_subscribes_but_has_not_vacancies(
    session
):
    """Проверяет пагинацию когда есть подписки на категории но нет вакансий"""
    subscribe_count: int = random.randint(3, 10)
    categories = []
    for _ in range(subscribe_count):
        category_name: str = f"Category {random.randint(1, 10000000000)}"
        category: Category = await create_category(
            session, 
            CreateCategoryRequest(name = category_name)
        )
        categories.append(category)

    user: User = await get_user_by_id(
        session, 
        user_id=(await create_tg_user_with_session(session)).id
    )
    user.categories.extend(categories)
    await session.commit()

    result = await fetch_vacancies_for_the_week(
        session,
        user,
        PAGE,
        PAGE_SIZE
    )
        
    assert result.get('status') == VacanciesForTheWeekStatusEnum.VACANCY_LIST_EMPTY