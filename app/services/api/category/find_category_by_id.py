from exceptions.category.category_not_found_error import CategoryNotFoundError
from models.category import Category
from query_objects.categories.get_category_by_id import get_category_by_id
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
        CategoryNotFoundError: Категория с ID {category_id} не найдена
    """
    category: Category = await get_category_by_id(db, category_id.id)

    if not category:
        raise CategoryNotFoundError(category_id.id)

    return category
