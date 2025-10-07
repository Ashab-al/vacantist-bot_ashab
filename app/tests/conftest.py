import os
import sys
from pathlib import Path
from typing import AsyncGenerator

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import (  # noqa: E501
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from schemas.tg.user.tg_user import TgUser
from models.user import User
import random

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


def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption(
        "--run-integration",
        action="store_true",
        default=False,
        help="run integration tests",
    )


def pytest_configure(config: pytest.Config) -> None:
    config.addinivalue_line(
        "markers",
        "integration: mark test as requiring --run-integration to run",
    )


def pytest_collection_modifyitems(
    config: pytest.Config, items: list[pytest.Item]
) -> None:
    if config.getoption("--run-integration"):
        return
    skip_integration = pytest.mark.skip(
        reason="need --run-integration option to run",
    )
    for item in items:
        if "integration" in item.keywords:
            item.add_marker(skip_integration)


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
async def new_tg_user(session_factory) -> User:
    return await create_tg_user(session_factory)

async def create_tg_user(session_factory):
    """Возвращает нового пользователя для тестов"""
    user_data: dict[str, str | int] = {
        "id": random.randint(1000, 100000000),
        "first_name": f"Имя {random.randint(1, 1000)}",
        "username": f"asd{random.randint(1, 1000)}"
    }
    new_user_schema: TgUser = TgUser.model_validate(user_data)
    async with session_factory() as session:
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