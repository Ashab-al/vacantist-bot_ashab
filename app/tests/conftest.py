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
