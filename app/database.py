from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, AsyncAttrs, async_sessionmaker
from config import settings
from datetime import datetime
from typing import AsyncGenerator

database_url: str = settings.database_dsn
engine = create_async_engine(
    url=database_url,
    echo="debug",
    pool_pre_ping=True
    
)
async_session_maker = async_sessionmaker(engine, class_=AsyncSession)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


class Base(AsyncAttrs, DeclarativeBase):
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())