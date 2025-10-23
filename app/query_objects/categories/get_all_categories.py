from models.category import Category
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


async def get_all_categories(db: AsyncSession) -> list[Category]:
    """
    Получить список всех категорий из базы данных.

    Args:
        db (AsyncSession): Асинхронная сессия SQLAlchemy для работы с базой данных.

    Returns:
        list[Category]: Список всех категорий.
    """
    result = await db.execute(select(Category))
    categories = result.scalars().all()
    return categories
