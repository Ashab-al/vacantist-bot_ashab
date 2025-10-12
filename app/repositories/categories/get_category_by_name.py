from models.category import Category
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


async def get_category_by_name(db: AsyncSession, name: str) -> Category | None:
    """
    Найти категорию по ее имени.

    Args:
        db (AsyncSession): Активная сессия БД.
        name (str): Название категории для поиска

    Returns:
        Category | None: Объект Category, если найден, иначе None
    """
    return (
        await db.execute(select(Category).where(Category.name == name))
    ).scalar_one_or_none()
