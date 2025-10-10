from datetime import datetime

from sqlalchemy import func
from sqlalchemy.ext.asyncio import (AsyncAttrs, AsyncSession,
                                    create_async_engine)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """
    Базовый класс для моделей SQLAlchemy.

    Все модели будут автоматически иметь поля:
        - created_at: Дата создания записи.
        - updated_at: Дата последнего обновления записи.
    """

    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), onupdate=func.now()
    )
