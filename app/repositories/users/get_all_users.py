from models.user import User
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

async def get_all_users(
    db: AsyncSession
) -> list[User]:
    users: list[User] = (
        await db.execute(
            select(User).options(joinedload(User.categories))
        )
    ).scalars().all()

    return users