from typing import Annotated

from database import get_async_session
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()


@router.post(
    "/mail_all",
    summary="Массовая отправка сообщения по базе",
    description="Отправляем всем пользователям сообщение",
)
async def mail_all(_session: Annotated[AsyncSession, Depends(get_async_session)]):
    """
    Массовая рассылка сообщений всем пользователям.

    Эндпоинт предназначен для отправки сообщения всем пользователям,
    которые хранятся в базе данных. Пока реализация отсутствует (TO DO).

    Args:
        session (AsyncSession): Асинхронная сессия SQLAlchemy для работы с базой данных.

    Returns:
        None: В текущей реализации ничего не возвращает.
        После реализации может возвращать объект с результатом рассылки.
    """
    # TO DO
