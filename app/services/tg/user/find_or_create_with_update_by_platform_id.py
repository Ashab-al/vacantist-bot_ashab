from models.user import User
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.tg.user.tg_user import TgUser
from repositories.users.get_user_by_platform_id import get_user_by_platform_id
from aiogram.types.user import User as AiogramTgUser
from enums.bot_status_enum import BotStatusEnum
from services.tg.send_analytics import send_analytics


async def find_or_create_with_update_by_platform_id(
    db: AsyncSession,
    user_data: AiogramTgUser
) -> User:
    
    user: User | None = await get_user_by_platform_id(
        db,
        user_data.id
    )
    if user:
        user.bot_status = BotStatusEnum.WORKS
    else:
        new_user_schema: TgUser = TgUser.model_validate(user_data)
        
        user: User = User(
            platform_id=new_user_schema.id,
            first_name=new_user_schema.first_name,
            username=new_user_schema.username,
            email=None,
            phone=None,
            point=new_user_schema.point,
            bonus=new_user_schema.bonus,
            bot_status=new_user_schema.bot_status
        )
        db.add(user)
        await send_analytics(db, user)

    await db.commit()
    await db.refresh(user)

    return user
    
