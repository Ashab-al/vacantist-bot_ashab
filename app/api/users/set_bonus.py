from fastapi import APIRouter, Depends, Path, Body, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_async_session
from typing import Annotated
from schemas.api.users.set_bonus.request import SetBonusUserIdRequest, SetBonusRequest
from schemas.api.users.set_bonus.response import SetBonusResponse
from services.api.user.set_bonus import set_bonus


router = APIRouter()

@router.post(
    "/{id}/set_bonus",
    summary='Обновить количество бонусов у пользователя',
    description='Обновляет количество бонусов у пользователя',
    response_model=SetBonusResponse
)
async def update_bonus(
    session: Annotated[AsyncSession, Depends(get_async_session)],
    bonus: Annotated[SetBonusRequest, Body()],
    user_id: Annotated[SetBonusUserIdRequest, Path()]
):
    try:
        user = await set_bonus(session, user_id, bonus)
    except ValueError as e:
        raise HTTPException(400, str(e))

    return user