from fastapi import Depends, APIRouter, Body, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_async_session
from typing import Annotated


router = APIRouter()

@router.post(
    "/",
    summary='Получить все категории',
    description='Возвращает все категории которые есть'
)
async def list_categories():
    ...