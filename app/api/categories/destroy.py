from typing import Annotated

from database import get_async_session
from fastapi import APIRouter, Depends, HTTPException, Path
from schemas.api.categories.destroy import (
    DestroyCategoryRequest,
    DestroyCategoryResponse,
)
from services.api.category.delete_category import delete_category
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()


@router.delete(
    "/{id}",
    summary="Удалить категорию",
    description="Удаляет категорию категорию",
    response_model=DestroyCategoryResponse,
)
async def destroy_category(
    session: Annotated[AsyncSession, Depends(get_async_session)],
    category_id: Annotated[DestroyCategoryRequest, Path()],
):
    """
    Удаляет категорию по её ID.

    Args:
        session (AsyncSession): Асинхронная сессия SQLAlchemy.
        id (int): ID категории, которую необходимо удалить.

    Returns:
        DestroyCategoryResponse: Информация об удалённой категории.

    Raises:
        ValueError: Категории не существует
    """
    try:
        category = await delete_category(session, category_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(
            detail=f"InternalServerError {str(e)}", status_code=500
        ) from e

    return category
