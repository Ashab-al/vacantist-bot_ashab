from sqlalchemy import (
    select
)
from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession
from models.category import Category
from models.subscription import subscription

async def advertisement(
    db: AsyncSession        
):
    result = await db.execute(
        select(Category.name, func.count(subscription.c.user_id))
        .join(subscription, subscription.c.category_id == Category.id)
        .group_by(Category.id)
    )
    return result.all()