from aiogram.types.user import User as AiogramTgUser
from exceptions.user_already_exist_error import UserAlreadyExistError
from models.user import User
from query_objects.users.get_user_by_platform_id import get_user_by_platform_id
from schemas.tg.user.tg_user import TgUser
from sqlalchemy.ext.asyncio import AsyncSession


async def create_user(db: AsyncSession, user_data: AiogramTgUser) -> User:
    """
    Создать нового пользователя в базе данных по его Telegram `platform_id`.
    Если пользователь с таким `platform_id` уже существует, поднимает исключение.

    Args:
        db (AsyncSession): Асинхронная сессия SQLAlchemy для работы с базой данных.
        user_data (AiogramTgUser): Объект пользователя телеграм

    Returns:
        User: Объект пользователя, созданный в базе данных.

    Raises:
        UserAlreadyExistError: Если пользователь с таким `platform_id` уже существует.
    """
    user: User | None = await get_user_by_platform_id(db, user_data.id)
    if user:
        raise UserAlreadyExistError(user_data.id)

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

    await db.commit()
    await db.refresh(user)

    return user
