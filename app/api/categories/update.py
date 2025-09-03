from fastapi import Depends, APIRouter, Body, HTTPException, Path
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_async_session
from typing import Annotated
from schemas.api.categories.update.request import UpdateCategoryRequest
from schemas.api.categories.update.response import UpdateCategoryResponse
from services.api.category.update_category import update_category

router = APIRouter()

@router.patch(
    "/{category_id}",
    summary='Обновить категорию',
    description='Обновляет категорию',
    response_model=UpdateCategoryResponse
)
async def update(
    category_data: Annotated[UpdateCategoryRequest, Body()],
    category_id: Annotated[int, Path()],
    session: Annotated[AsyncSession, Depends(get_async_session)]
):
    try:
        category = await update_category(
            session,
            category_id,
            category_data
        )
    except ValueError as e:
        raise HTTPException(400, str(e))
    
    return category
