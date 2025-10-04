from fastapi import Depends, APIRouter
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
    """
    Возвращает список всех категорий.

    Args:
        session (AsyncSession): Асинхронная сессия SQLAlchemy.

    Returns:
        ListCategoryResponse: Список всех категорий.
    """
    categories = await categories_list(session)

    return ListCategoryResponse(categories=categories)