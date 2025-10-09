import random
from httpx import AsyncClient
import pytest
from models.category import Category
from models.user import User
from repositories.users.get_user_by_id import get_user_by_id
from schemas.api.categories.create.request import CreateCategoryRequest
from services.api.category.create_category import create_category
from tests.conftest import create_tg_user_with_session
from services.tg.advertisement import advertisement
import pytest_asyncio


@pytest.mark.asyncio
async def test_create_category(client):
    response = await client.post("/api/v1/categories/", json={"name": "Test"})
    assert response.status_code == 200