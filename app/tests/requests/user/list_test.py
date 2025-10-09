import random
import pytest
from tests.conftest import create_tg_user
from models.user import User

@pytest.mark.asyncio
async def test_list_users(
    client, 
    session
):
    """Тестирует эндпоинт возврата списка всех существующих пользователей"""
    users_count: int = random.randint(4, 10)

    users: list[User] = [
        await create_tg_user(session)
        for _ in range(users_count)    
    ]
        
    response = await client.get(
        "/users/"
    )

    assert response.status_code == 200
    assert len(response.json().get('users')) == len(users)
    assert {user.get('platformId') for user in response.json().get('users')} == {user.platform_id for user in users}

