from fastapi import Depends, APIRouter, Body, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_async_session
from typing import Annotated


router = APIRouter()

@router.post(
    "/",
    summary='Удалить категорию',
    description='Удаляет категорию категорию'
)
async def destroy_category():
    ...