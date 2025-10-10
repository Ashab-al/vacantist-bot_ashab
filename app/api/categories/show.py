from fastapi import Depends, APIRouter, Path, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_async_session
from typing import Annotated
from schemas.api.categories.show.response import ShowCategoryResponse
from schemas.api.categories.show.request import ShowCategoryRequest
from services.api.category.find_category_by_id import find_category_by_id


router = APIRouter()


@router.get(
    "/{id}",
    summary="Получить категорию",
    description="Возвращает информацию о категории",
    response_model=ShowCategoryResponse,
)
async def show_category(
    session: Annotated[AsyncSession, Depends(get_async_session)],
    category_id: Annotated[ShowCategoryRequest, Path()],
):
    """
    Возвращает категорию по её ID.

    Args:
        session (AsyncSession): Асинхронная сессия SQLAlchemy.
        id (int): ID категории для получения информации.

    Returns:
        ShowCategoryResponse: Информация о найденной категории.

    Raises:
        HTTPException: Если категория с указанным ID не найдена.
    """
    try:
        category = await find_category_by_id(session, category_id)
    except ValueError as e:
        raise HTTPException(404, str(e))

    return category
