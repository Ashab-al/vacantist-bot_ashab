from models.category import Category
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


async def get_all_categories(
    db: AsyncSession
) -> list[Category]:
    categories: list[Category] = (
        await db.execute(
            select(Category)
        )
    ).scalars().all()

    return categories