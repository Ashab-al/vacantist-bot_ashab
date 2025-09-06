from fastapi import Depends, APIRouter, Body, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_async_session
from typing import Annotated
from services.api.category.categories_list import categories_list
from schemas.api.categories.list.response import ListCategoryResponse


router = APIRouter()

@router.get(
    "/",
    summary='Получить все категории',
    description='Возвращает все категории которые есть',
    response_model=ListCategoryResponse
)
async def list_categories(
    session: Annotated[AsyncSession, Depends(get_async_session)]
):
    categories = await categories_list(session)

    return ListCategoryResponse(categories=categories)