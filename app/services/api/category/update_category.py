from exceptions.category.category_not_found_error import CategoryNotFoundError
from models.category import Category
from query_objects.categories.get_category_by_id import get_category_by_id
from schemas.api.categories.update.request import UpdateCategoryRequest
from sqlalchemy.ext.asyncio import AsyncSession


async def update_category(
    db: AsyncSession, category_id: int, category_data: UpdateCategoryRequest
) -> Category:
    """
    Обновляет категорию по `id` категории

    Args:
        db (AsyncSession): Асинхронная сессия SQLAlchemy для работы с базой данных
        category_id (int): `id` категории
        category_data (UpdateCategoryRequest): Схема для обновления категории

    Returns:
        Category: Обновленная категория

    Raises:
        CategoryNotFoundError: Категория с ID {self.category_id} не найдена
    """
    category: Category | None = await get_category_by_id(db, category_id)

    if not category:
        raise CategoryNotFoundError(category_id)

    category.name = category_data.name
    db.add(category)
    await db.commit()
    await db.refresh(category)

    return category
