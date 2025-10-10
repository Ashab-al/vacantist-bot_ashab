from models.category import Category
from schemas.api.categories.destroy import DestroyCategoryRequest
from sqlalchemy import select
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
    category: Category | None = (
        await db.execute(select(Category).where(Category.id == category_id.id))
    ).scalar_one_or_none()  # TODO Перенести в репозиторий либо вызывать сервис

    if category is None:
        raise ValueError("Категории не существует")

    await db.delete(category)
    await db.commit()

    return category
