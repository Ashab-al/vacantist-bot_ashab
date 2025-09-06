from fastapi import Depends, APIRouter, Body, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_async_session
from typing import Annotated
from schemas.api.categories.create.request import CreateCategoryRequest
from schemas.api.categories.create.response import CreateCategoryResponse
from services.api.category.create_category import create_category

router = APIRouter()

@router.post(
    "/",
    summary='Создать категорию',
    description='Создает новую категорию',
    response_model=CreateCategoryResponse
)
async def create_new_category(
    session: Annotated[AsyncSession, Depends(get_async_session)],
    category_data: Annotated[CreateCategoryRequest, Body()]
):
    try:
        category: CreateCategoryResponse = await create_category(
            session, 
            category_data
        )
    except Exception as e:
        raise HTTPException(400, str(e))
    
    return category