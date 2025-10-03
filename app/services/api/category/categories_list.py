from models.category import Category
from repositories.categories.get_all_categories import get_all_categories
from sqlalchemy.ext.asyncio import AsyncSession


async def categories_list(
    db: AsyncSession
) -> list[Category]:
    """
    Возвращает список всех категорий

    Args:
        db (AsyncSession): Асинхронная сессия SQLAlchemy для работы с базой данных
    Returns:
        list[Category]: Список категорий
    """
    return await get_all_categories(db)