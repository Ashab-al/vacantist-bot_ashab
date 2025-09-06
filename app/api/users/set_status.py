from fastapi import APIRouter, Depends, Path, Body, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_async_session
from typing import Annotated
from schemas.api.users.set_status.request import SetStatusUserIdRequest, SetStatusRequest
from services.api.user.set_status import set_status
from schemas.api.users.set_status.response import SetStatusResponse

router = APIRouter()

@router.post(
    "/{id}/set_status",
    summary='Изменить статус пользователя в боте',
    description='Изменяет статус пользователя в боте. Возможные значения: `WORKS`, `BOT_BLOCKED`',
    response_model=SetStatusResponse
)
async def update_status(
    session: Annotated[AsyncSession, Depends(get_async_session)],
    user_id: Annotated[SetStatusUserIdRequest, Path()],
    bot_status: Annotated[SetStatusRequest, Body()]
):
    try:
        user = await set_status(session, user_id, bot_status)
    except ValueError as e:
        raise HTTPException(400, str(e))
    
    return user
