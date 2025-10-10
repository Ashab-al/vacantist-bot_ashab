from models.user import User
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.tg.user.tg_user import TgUser
from repositories.users.get_user_by_platform_id import get_user_by_platform_id
from aiogram.types.user import User as AiogramTgUser
from enums.bot_status_enum import BotStatusEnum
from services.tg.send_analytics import send_analytics


async def find_or_create_with_update_by_platform_id(
    db: AsyncSession, user_data: AiogramTgUser
) -> User:
    """
    Найти пользователя по его Telegram `platform_id` или создать нового.

    Если пользователь существует и его статус `WORKS` — сразу возвращает пользователя
    Если пользователь существует и его статус `BOT_BLOCKED` — обновляется его атрибут `bot_status` на `WORKS`.
    Если пользователь новый — создаётся запись в базе и отправляется уведомление
    в группу администратора через `send_analytic

    Args:
        db (AsyncSession): Асинхронная сессия SQLAlchemy для работы с базой данных.
        user_data (AiogramTgUser): Объект пользователя телеграм

    Returns:
        User: Объект пользователя, найденный или созданный в базе данных.
    """
    user: User | None = await get_user_by_platform_id(db, user_data.id)

    if user and user.bot_status == BotStatusEnum.WORKS:
        return user
    elif user and user.bot_status == BotStatusEnum.BOT_BLOCKED:
        user.bot_status = BotStatusEnum.WORKS
    elif not user:
        new_user_schema: TgUser = TgUser.model_validate(user_data)

        user: User = User(
            platform_id=new_user_schema.id,
            first_name=new_user_schema.first_name,
            username=new_user_schema.username,
            email=new_user_schema.email,
            phone=new_user_schema.phone,
            point=new_user_schema.point,
            bonus=new_user_schema.bonus,
            bot_status=new_user_schema.bot_status,
        )
        db.add(user)

        await send_analytics(db, user)

    await db.commit()
    await db.refresh(user)

    return user
