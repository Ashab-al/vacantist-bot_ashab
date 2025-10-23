import sys
from pathlib import Path
from unittest.mock import AsyncMock

import pytest
import pytest_asyncio

# Добавляем импорт модули Categories
from api.categories import categories_router
from api.categories import create as categories_create_module  # noqa: E402
from api.categories import destroy as categories_destroy_module  # noqa: E402
from api.categories import list as categories_list_module  # noqa: E402
from api.categories import show as categories_show_module  # noqa: E402
from api.categories import update as categories_update_module  # noqa: E402

# Добавляем импорт модулей Users
from api.users import list as users_list_module  # noqa: E402
from api.users import mail_all as users_mail_all_module  # noqa: E402
from api.users import set_bonus as users_set_bonus_module  # noqa: E402
from api.users import set_status as users_set_status_module  # noqa: E402
from api.users import show as users_show_module  # noqa: E402
from api.users import users_router

# Добавляем импорт модули Vacancies
from api.vacancies import create as vacancies_create_module  # noqa: E402
from api.vacancies import list as vacancies_list_module  # noqa: E402
from api.vacancies import vacancies_router
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))


async def remove_response_model_in_router(router):
    """Убираем response_model из роутеров"""
    for route in router.routes:
        route.response_model = None
    return router


@pytest_asyncio.fixture
async def app(session_mock: AsyncMock) -> FastAPI:  # noqa: W0621
    """Создаем тестовый FastAPI app"""
    new_app = FastAPI()

    new_app.include_router(
        await remove_response_model_in_router(categories_router), prefix="/categories"
    )

    new_app.include_router(
        await remove_response_model_in_router(users_router), prefix="/users"
    )

    new_app.include_router(
        await remove_response_model_in_router(vacancies_router), prefix="/vacancies"
    )

    async def _override_get_async_session():
        """Мокаем зависимость get_async_session"""
        yield session_mock

    new_app.dependency_overrides[categories_create_module.get_async_session] = (
        _override_get_async_session
    )
    new_app.dependency_overrides[categories_destroy_module.get_async_session] = (
        _override_get_async_session
    )
    new_app.dependency_overrides[categories_list_module.get_async_session] = (
        _override_get_async_session
    )
    new_app.dependency_overrides[categories_show_module.get_async_session] = (
        _override_get_async_session
    )
    new_app.dependency_overrides[categories_update_module.get_async_session] = (
        _override_get_async_session
    )

    new_app.dependency_overrides[users_list_module.get_async_session] = (
        _override_get_async_session
    )
    new_app.dependency_overrides[users_mail_all_module.get_async_session] = (
        _override_get_async_session
    )
    new_app.dependency_overrides[users_set_bonus_module.get_async_session] = (
        _override_get_async_session
    )
    new_app.dependency_overrides[users_set_status_module.get_async_session] = (
        _override_get_async_session
    )
    new_app.dependency_overrides[users_show_module.get_async_session] = (
        _override_get_async_session
    )

    new_app.dependency_overrides[vacancies_create_module.get_async_session] = (
        _override_get_async_session
    )
    new_app.dependency_overrides[vacancies_list_module.get_async_session] = (
        _override_get_async_session
    )

    return new_app


@pytest.fixture
def session_mock() -> AsyncMock:
    """Мокаем сессию"""
    return AsyncMock()


@pytest_asyncio.fixture
async def client(app: FastAPI):
    """Создаем тестовый клиент для FastAPI app"""
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        yield client
