from exceptions.category.category_already_exist_error import CategoryAlreadyExistError
from models.category import Category
from query_objects.categories.get_category_by_name import get_category_by_name
from schemas.api.categories.create import CreateCategoryRequest
from sqlalchemy.ext.asyncio import AsyncSession


async def create_category(
    db: AsyncSession, category_data: CreateCategoryRequest
) -> Category:
    """
    Создает новую категорию

    Args:
        db (AsyncSession): Асинхронная сессия SQLAlchemy для работы с базой данных
        category_data (CreateCategoryRequest): Схема для создания категории

    Returns:
        category (Category): Объект категории

    Raises:
        CategoryAlreadyExistError: Такая категория уже существует
    """
    category: Category | None = await get_category_by_name(db, category_data.name)

    if category:
        raise CategoryAlreadyExistError()

    category: Category = Category(name=category_data.name)
    db.add(category)
    await db.commit()
    await db.refresh(category)

    return category
