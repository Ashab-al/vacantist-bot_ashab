from fastapi import Depends, APIRouter, Path, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_async_session
from typing import Annotated
from services.api.category.delete_category import delete_category
from schemas.api.categories.destroy.request import DestroyCategoryRequest
from schemas.api.categories.destroy.response import DestroyCategoryResponse


router = APIRouter()

@router.delete(
    "/{id}",
    summary='Удалить категорию',
    description='Удаляет категорию категорию',
    response_model=DestroyCategoryResponse
)
async def destroy_category(
    session: Annotated[AsyncSession, Depends(get_async_session)],
    category_id: Annotated[DestroyCategoryRequest, Path()]
):
    category = await delete_category(
        session,
        category_id
    )

    return category
