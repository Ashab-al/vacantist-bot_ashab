from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_async_session
from schemas.api.users.show.response import ShowUserResponse
from schemas.api.users.show.request import ShowUserRequest
from typing import Annotated
from services.api.user.find_user_by_id import find_user_by_id


router = APIRouter()

@router.get(
    '/{id}',
    summary='Получить пользователя по id',
    description='Возвращает пользователя по id',
    response_model=ShowUserResponse
)
async def show(
    session: Annotated[AsyncSession, Depends(get_async_session)],
    user_id: Annotated[ShowUserRequest, Path()]
):
    try:
        user = await find_user_by_id(
            session, 
            user_id
        )
    except ValueError as e:
        raise HTTPException(400, str(e))

    return user