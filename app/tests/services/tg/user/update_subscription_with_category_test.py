import pytest
import random
from models.user import User
from repositories.users.get_user_by_id import get_user_by_id
from services.tg.user.update_subscription_with_category import update_subscription_with_category
from bot.filters.callback.category_callback import CategoryCallback
from enums.category_subscription_enum import CategorySubscriptionEnum
from tests.conftest import create_tg_user_with_session, create_vacancy_and_category_with_session



@pytest.mark.asyncio
async def test_update_subscription_with_category_when_user_has_subscribe(
    session
):
    """Проверка подписки / отписки на категорию. 
    Случай когда пользователь изначально был подписан на категорию
    """
    subscribe_count: int = random.randint(3, 10)
    categories = []
    for _ in range(subscribe_count):
        _vacancy, category = await create_vacancy_and_category_with_session(session)
        categories.append(category)

    user: User = await get_user_by_id(
        session, 
        user_id=(await create_tg_user_with_session(session)).id
    )
    
    user.categories.extend(categories)
    
    await session.commit()

    result: dict[str, str] = await update_subscription_with_category(
        CategoryCallback(category_id=categories[0].id),
        session,
        user.categories,
        user
    )
    
    assert result.get('path_to_templates') == CategorySubscriptionEnum.UNSUBSCRIBE.value

@pytest.mark.asyncio
async def test_update_subscription_with_category_when_user_has_not_subscribe(
    session
):
    """Проверка подписки / отписки на категорию. 
    Случай когда пользователь изначально не был подписан на категорию
    """
    subscribe_count: int = random.randint(3, 10)
    categories = []
    for _ in range(subscribe_count):
        _vacancy, category = await create_vacancy_and_category_with_session(session)
        categories.append(category)

    user: User = await get_user_by_id(
        session, 
        user_id=(await create_tg_user_with_session(session)).id
    )
    
    result: dict[str, str] = await update_subscription_with_category(
        CategoryCallback(category_id=categories[0].id),
        session,
        user.categories,
        user
    )
    
    assert result.get('path_to_templates') == CategorySubscriptionEnum.SUBSCRIBE.value