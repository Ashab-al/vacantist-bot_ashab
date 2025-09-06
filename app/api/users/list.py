from fastapi import APIRouter, Depends, Body, Path, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_async_session
from typing import Annotated
from schemas.api.users.list.response import ListUsersResponse
from services.api.user.users_list import users_list

router = APIRouter()

@router.get(
    '/',
    summary='Получить всех пользователей',
    description='Возвращает список всех пользователей',
    response_model=ListUsersResponse
)
async def list_users(
    session: Annotated[AsyncSession, Depends(get_async_session)]
):
    users = await users_list(session)

    return ListUsersResponse(users=users)