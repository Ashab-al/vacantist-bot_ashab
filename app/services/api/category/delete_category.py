from models.category import Category
from sqlalchemy.ext.asyncio import AsyncSession
from models.category import Category
from sqlalchemy import (
    select,
)


async def delete_category(
    db: AsyncSession,
    category_id: int
) -> Category:
    category = (
        await db.execute(select(Category).where(Category.id == category_id.id))
    ).scalar_one_or_none()

    if category:
        await db.delete(category)
        await db.commit()
    
    return category