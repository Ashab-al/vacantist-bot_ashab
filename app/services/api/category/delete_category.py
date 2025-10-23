from exceptions.category.category_not_found_error import CategoryNotFoundError
from models.category import Category
from query_objects.categories.get_category_by_id import get_category_by_id
from schemas.api.categories.destroy import DestroyCategoryRequest
from sqlalchemy.ext.asyncio import AsyncSession


async def delete_category(
    db: AsyncSession, category_id: DestroyCategoryRequest
) -> Category:
    """
    Удалить категорию по `id` категории

    Args:
        db (AsyncSession): Асинхронная сессия SQLAlchemy для работы с базой данных
        category_id (DestroyCategoryRequest): схема для удаления категории

    Returns:
        category (Category): Категория, которая была удалена.

    Raises:
        ValueError: Категории не существует
    """
    category: Category | None = await get_category_by_id(db, category_id.id)

    if category is None:
        raise CategoryNotFoundError(category_id.id)

    await db.delete(category)
    await db.commit()

    return category
