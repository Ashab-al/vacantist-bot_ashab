from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from models.category import Category
from models.subscription import subscription


async def advertisement(
    db: AsyncSession        
) -> list[tuple[str, int]]:
    """
    Получает количество подписчиков для каждой категории.

    Args:
        db (AsyncSession): Асинхронная сессия SQLAlchemy для выполнения запросов.

    Returns:
        list[tuple[str, int]]: Список кортежей, где первый элемент — название категории,
        а второй — количество подписчиков.
    """
    result = await db.execute(
        select(Category.name, func.count(subscription.c.user_id))
        .join(subscription, subscription.c.category_id == Category.id)
        .group_by(Category.id)
    )
    return result.all()