from sqlalchemy.ext.asyncio import AsyncSession
from models.category import Category
from schemas.api.categories.create.response import CreateCategoryResponse
from schemas.api.categories.create.request import CreateCategoryRequest
from repositories.categories.get_category_by_name import get_category_by_name


async def create_category(
    db: AsyncSession,
    category_data: CreateCategoryRequest
) -> CreateCategoryResponse:
    """
    Создает новую категорию

    Args:
        db (AsyncSession): Асинхронная сессия SQLAlchemy для работы с базой данных
        category_data (CreateCategoryRequest): Схема для создания категории
    
    Returns:
        CreateCategoryResponse: Схема для возврата успешного ответа после создании категории
    
    Raises:
        ValueError: Такая категория уже существует

    """
    category: Category | None = await get_category_by_name(
        db, 
        category_data.name
    )

    if category:
        raise ValueError("Такая категория уже существует")

    category: Category = Category(name=category_data.name)
    db.add(category)
    await db.commit()
    await db.refresh(category)
    
    return category