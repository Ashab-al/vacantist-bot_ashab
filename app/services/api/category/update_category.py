from models.category import Category
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.api.categories.update.request import UpdateCategoryRequest

async def update_category(
    db: AsyncSession,
    category_id: int,
    category_data: UpdateCategoryRequest
) -> Category:
    category: Category = await db.get(Category, category_id)

    if not category:
        raise ValueError(f"Категории по id - {category_id} нет в базе")
    
    category.name = category_data.name
    db.add(category)
    await db.commit()
    await db.refresh(category)
    
    return category