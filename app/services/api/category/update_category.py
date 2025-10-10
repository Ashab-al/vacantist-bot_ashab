from models.category import Category
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
        ValueError: Категории по id - `category_id` нет в базе
    """
    category: Category = await db.get(Category, category_id)

    if not category:
        raise ValueError(f"Категории по id - {category_id} нет в базе")

    category.name = category_data.name
    db.add(category)
    await db.commit()
    await db.refresh(category)

    return category
