from typing import Annotated

from database import get_async_session
from fastapi import APIRouter, Body, Depends, HTTPException, Path
from schemas.api.users.set_status.request import (SetStatusRequest,
                                                  SetStatusUserIdRequest)
from schemas.api.users.set_status.response import SetStatusResponse
from services.api.user.set_status import set_status
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()


@router.post(
    "/{id}/set_status",
    summary="Изменить статус пользователя в боте",
    description="Изменяет статус пользователя в боте. Возможные значения: `WORKS`, `BOT_BLOCKED`",
    response_model=SetStatusResponse,
)
async def update_status(
    session: Annotated[AsyncSession, Depends(get_async_session)],
    user_id: Annotated[SetStatusUserIdRequest, Path()],
    bot_status: Annotated[SetStatusRequest, Body()],
):
    """
    Изменить статус пользователя в боте.

    Эндпоинт обновляет статус пользователя в системе.
    Доступные варианты статуса:
    - `WORKS` — пользователь активен;
    - `BOT_BLOCKED` — пользователь заблокировал бота.

    Args:
        session (AsyncSession): Асинхронная сессия SQLAlchemy для работы с базой данных.
        user_id (SetStatusUserIdRequest): Идентификатор пользователя, у которого нужно изменить статус.
        bot_status (SetStatusRequest): Новое значение статуса пользователя.

    Raises:
        HTTPException: Возвращает ошибку 400, если передан некорректный статус или пользователь не найден.

    Returns:
        SetStatusResponse: Обновлённые данные пользователя со статусом.
    """
    try:
        user = await set_status(session, user_id, bot_status)
    except ValueError as e:
        raise HTTPException(404, str(e))

    return user
