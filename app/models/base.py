from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, AsyncAttrs
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase
from datetime import datetime
from sqlalchemy import func


class Base(DeclarativeBase):
    """
    Базовый класс для моделей SQLAlchemy.

    Все модели будут автоматически иметь поля:
        - created_at: Дата создания записи.
        - updated_at: Дата последнего обновления записи.
    """
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())