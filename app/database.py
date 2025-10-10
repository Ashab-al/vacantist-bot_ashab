from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
    AsyncAttrs,
    async_sessionmaker,
)
from config import settings
from datetime import datetime
from typing import AsyncGenerator
from functools import wraps
from contextlib import asynccontextmanager

database_url: str = settings.database_dsn
"""URL базы данных"""

engine = create_async_engine(url=database_url, echo="debug", pool_pre_ping=True)
"""Асинхронный движок SQLAlchemy"""

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
            return await func(session=session, *args, **kwargs)

    return wrapper


# class Base(AsyncAttrs, DeclarativeBase):
#     """
#     Базовый класс для моделей SQLAlchemy.

#     Все модели будут автоматически иметь поля:
#         - created_at: Дата создания записи.
#         - updated_at: Дата последнего обновления записи.
#     """
#     created_at: Mapped[datetime] = mapped_column(server_default=func.now())
#     updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())
