from models.category import Category
from repositories.categories.get_all_categories import get_all_categories
from sqlalchemy.ext.asyncio import AsyncSession


async def categories_list(
    db: AsyncSession
) -> list:
    categories: list[Category] = await get_all_categories(db)

    return categories