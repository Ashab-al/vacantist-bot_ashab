from models.category import Category
from schemas.api.categories.show.request import ShowCategoryRequest
from sqlalchemy.ext.asyncio import AsyncSession


async def find_category_by_id(
    db: AsyncSession, category_id: ShowCategoryRequest
) -> Category:
    """
    Возвращает категорию по id категории

    Args:
        db (AsyncSession): Асинхронная сессия SQLAlchemy для работы с базой данных
        category_id (ShowCategoryRequest): Схема для возврата категории

    Returns:
        Category: Объект категории

    Raises:
        ValueError: Категории по id - `category_id.id` нет в базе
    """
    category: Category = await db.get(Category, category_id.id)

    if not category:
        raise ValueError(f"Категории по id - {category_id.id} нет в базе")

    return category
