import pytest
import pytest_asyncio
import os
import sys
from pathlib import Path
from fastapi import FastAPI
from httpx import AsyncClient, ASGITransport
from typing import AsyncGenerator
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch
from main import app as main_app
from database import get_async_session
from sqlalchemy.ext.asyncio import (  # noqa: E501
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from lib.tg.constants import SOURCE
from models.category import Category
from models.vacancy import Vacancy
from schemas.api.categories.create.request import CreateCategoryRequest
from schemas.api.vacancies.create.request import CreateVacancyRequest
from schemas.tg.user.tg_user import TgUser
from models.user import User
import random

from services.api.category.create_category import create_category
from services.api.vacancy.create_vacancy import create_vacancy

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from models.base import Base  # noqa: E402



def _load_env(path: str) -> None:
    """Load key=value pairs from *path* if file exists."""

    file = Path(path)
    if not file.exists():
        return
    for line in file.read_text().splitlines():
        if not line or line.startswith("#"):
            continue
        key, _, value = line.partition("=")
        os.environ.setdefault(key, value)


_load_env(".env.test")


@pytest_asyncio.fixture
async def session_factory() -> AsyncGenerator[async_sessionmaker[AsyncSession], None]:
    """Provide a new in-memory SQLite session factory."""

    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    factory = async_sessionmaker(engine, expire_on_commit=False)
    yield factory
    await engine.dispose()

@pytest_asyncio.fixture
async def session(session_factory):
    async with session_factory() as session:
        yield session

@pytest_asyncio.fixture
async def app(
    session_factory: AsyncGenerator[async_sessionmaker[AsyncSession], None]
) -> FastAPI:
    async def _override_get_async_session():
        async with session_factory() as session:
            yield session
    
    main_app.dependency_overrides[get_async_session] = _override_get_async_session
    
    return main_app

@pytest_asyncio.fixture
async def client(app: FastAPI):
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test/api/v1") as client:
        yield client


@pytest_asyncio.fixture
async def new_tg_user(session_factory) -> User:
    async with session_factory() as session:
        return await create_tg_user(session)

async def create_tg_user(session):
    """Возвращает нового пользователя для тестов"""
    return await create_tg_user_with_session(session)

async def create_tg_user_with_session(session) -> User:
    """Возвращает нового пользователя для тестов"""
    user_data: dict[str, str | int] = {
        "id": random.randint(1000, 100000000),
        "first_name": f"Имя {random.randint(1, 1000)}",
        "username": f"asd{random.randint(1, 1000)}"
    }
    new_user_schema: TgUser = TgUser.model_validate(user_data)
    user: User = User(
        platform_id=new_user_schema.id,
        first_name=new_user_schema.first_name,
        username=new_user_schema.username,
        email=new_user_schema.email,
        phone=new_user_schema.phone,
        point=new_user_schema.point,
        bonus=new_user_schema.bonus,
        bot_status=new_user_schema.bot_status
    )
    session.add(user)
    await session.commit()
    await session.refresh(user)

    return user

async def create_vacancy_and_category(
    session
) -> tuple[Vacancy, Category]:
    """Создать и вернуть новую вакансию с рандомной категорией"""
    return await create_vacancy_and_category_with_session(session)


async def create_vacancy_and_category_with_session(
    session: AsyncSession
) -> tuple[Vacancy, Category]:
    """Создать и вернуть новую вакансию с рандомной категорией"""
    category_name: str = f"Category {random.randint(1, 10000000000)}"
    vacancy_data: dict[str, str] = {
        "title": category_name,
        "categoryTitle": category_name,
        "description": f"Описание вакансии{random.randint(100, 1000000)}",
        "contactInformation": f"ТГ - @username{random.randint(100, 1000000)}",
        "source": SOURCE,
        "platformId": f"{random.randint(100, 1000000)}"
    }
    create_vacancy_request: CreateVacancyRequest = CreateVacancyRequest(**vacancy_data)
    
    category: Category = await create_category(
        session, 
        CreateCategoryRequest(name = category_name)
    )
    vacancy: Vacancy = await create_vacancy(
        session,
        create_vacancy_request,
        category
    )
    
    return vacancy, category