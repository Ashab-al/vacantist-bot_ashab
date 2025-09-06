from models.category import Category
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from schemas.api.categories.show.request import ShowCategoryRequest


async def find_category_by_id(
    db: AsyncSession,
    category_id: ShowCategoryRequest
) -> Category:
    category: Category = await db.get(Category, category_id.id)

    if not category:
        raise ValueError(f"Категории по id - {category_id.id} нет в базе")

    return category