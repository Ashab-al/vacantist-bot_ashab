from models.category import Category
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


async def get_category_by_id(
    db: AsyncSession,
    category_id: int
) -> Category | None:
    """
    Найти категорию по id.

    Args:
        db (AsyncSession): Активная сессия БД.
        category_id (int): Id категории для поиска
    
    Returns:
        Category | None: Объект Category, если найден, иначе None
    """
    return (
        await db.execute(
            select(Category).where(Category.id == category_id)
        )
    ).scalar_one_or_none()