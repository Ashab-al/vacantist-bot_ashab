from contextlib import asynccontextmanager
from functools import wraps
from typing import AsyncGenerator

from config import settings
from enums.mode_enum import ModeEnum
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

database_url: str = settings.database_dsn
"""URL базы данных"""
engine = None
"""Асинхронный движок SQLAlchemy"""
if settings.mode == ModeEnum.DEVELOP:
    engine = create_async_engine(url=database_url, echo="debug", pool_pre_ping=True)
elif settings.mode == ModeEnum.PRODUCTION:
    engine = create_async_engine(url=database_url, echo=False, pool_pre_ping=True)

# Фабрика асинхронных сессий
async_session_maker = async_sessionmaker(engine, class_=AsyncSession)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Асинхронный генератор сессий для FastAPI через Depends.

    Yields:
        AsyncSession: Асинхронная сессия SQLAlchemy.
    """
    async with async_session_maker() as session:
        yield session


@asynccontextmanager
async def get_async_session_for_bot() -> AsyncGenerator[AsyncSession, None]:
    """
    Асинхронный контекстный менеджер для использования с ботом.

    Yields:
        AsyncSession: Асинхронная сессия SQLAlchemy.
    """
    async with async_session_maker() as session:
        yield session


def with_session(func):
    """
    Декоратор для хендлеров бота, чтобы автоматически прокидывать сессию.

    Args:
        func (Callable): Асинхронная функция-хендлер бота.

    Returns:
        Callable: Обернутая функция с прокинутой сессией.
    """

    @wraps(func)
    async def wrapper(*args, **kwargs):
        async with get_async_session_for_bot() as session:
            kwargs["session"] = session
            return await func(*args, **kwargs)

    return wrapper
