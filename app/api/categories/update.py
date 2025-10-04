from fastapi import Depends, APIRouter, Body, HTTPException, Path
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_async_session
from typing import Annotated
from schemas.api.categories.update import UpdateCategoryRequest, UpdateCategoryResponse
from services.api.category.update_category import update_category


router = APIRouter()

@router.patch(
    "/{category_id}",
    summary='Обновить категорию',
    description='Обновляет категорию',
    response_model=UpdateCategoryResponse,
    responses={
        400: {"description": "Невалидные данные"},
        404: {"description": "Категория не найдена"},
    }
)
async def update(
    category_data: Annotated[UpdateCategoryRequest, Body()],
    category_id: Annotated[int, Path()],
    session: Annotated[AsyncSession, Depends(get_async_session)]
):
    """
    Обновить категорию по её ID.

    Args:
        category_data (UpdateCategoryRequest): Данные для обновления категории.
        category_id (int): Идентификатор категории, которую требуется обновить.
        session (AsyncSession): Асинхронная сессия SQLAlchemy для работы с базой данных.

    Returns:
        UpdateCategoryResponse: Обновлённая категория.

    Raises:
        HTTPException: 400 — если данные некорректны.  
        HTTPException: 404 — если категория с указанным ID не найдена.
    """
    try:
        category = await update_category(
            session,
            category_id,
            category_data
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    
    return category
