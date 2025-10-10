from aiogram.types import CallbackQuery, ChatMemberUpdated, Message
from models.user import User
from services.tg.user.find_or_create_with_update_by_platform_id import \
    find_or_create_with_update_by_platform_id
from sqlalchemy.ext.asyncio import AsyncSession


async def current_user(
    session: AsyncSession,
    message: Message = None,
    query: CallbackQuery = None,
    event: ChatMemberUpdated = None,
) -> User:
    """
    Получает или создаёт пользователя в базе данных по данным из Telegram-объекта.

    Функция принимает один из объектов Telegram (Message, CallbackQuery или ChatMemberUpdated),
    извлекает из него данные о пользователе (`from_user`), и затем выполняет поиск
    или создание записи в базе данных, обновляя данные пользователя при необходимости.

    Args:
        session (AsyncSession): Асинхронная сессия SQLAlchemy для работы с базой данных.
        message (Message, optional): Сообщение Telegram, из которого может быть получен пользователь.
        query (CallbackQuery, optional): Callback-запрос Telegram, содержащий пользователя.
        event (ChatMemberUpdated, optional): Событие изменения состояния участника чата.

    Returns:
        User: Объект пользователя, найденный или созданный в базе данных.
    """
    source = message or query or event

    user: User = await find_or_create_with_update_by_platform_id(
        db=session, user_data=source.from_user
    )
    return user
