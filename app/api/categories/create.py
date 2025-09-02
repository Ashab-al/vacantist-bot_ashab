from fastapi import Depends, APIRouter, Body, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_async_session
from typing import Annotated


router = APIRouter()

@router.post(
    "/",
    summary='Создать категорию',
    description='Создает новую категорию'
)
async def create_category():
    ...