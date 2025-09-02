from fastapi import Depends, APIRouter, Body, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_async_session
from typing import Annotated


router = APIRouter()

@router.patch(
    "/",
    summary='Обновить категорию',
    description='Обновляет категорию'
)
async def update_category():
    ...