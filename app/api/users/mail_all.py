from fastapi import APIRouter, Depends, Path, Body, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_async_session
from typing import Annotated


router = APIRouter()

@router.post(
    "/mail_all",
    summary='Массовая отправка сообщения по базе',
    description='Отправляем всем пользователям сообщение'
)
async def mail_all(
    session: Annotated[AsyncSession, Depends(get_async_session)]  
):
    # TO DO
    ...