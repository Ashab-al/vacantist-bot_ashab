from typing import Annotated

from database import get_async_session
from exceptions.category.category_already_exist_error import CategoryAlreadyExistError
from fastapi import APIRouter, Body, Depends, HTTPException
from schemas.api.categories.create import CreateCategoryRequest, CreateCategoryResponse
from services.api.category.create_category import create_category
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()


@router.post(
    "/",
    summary="Создать категорию",
    description="Создает новую категорию",
    response_model=CreateCategoryResponse,
)
async def create_new_category(
    session: Annotated[AsyncSession, Depends(get_async_session)],
    category_data: Annotated[CreateCategoryRequest, Body()],
):
    """
    Создает новую категорию вакансий.

    Args:
        session (AsyncSession): Асинхронная сессия SQLAlchemy.
        category_data (CreateCategoryRequest): Данные для создания категории.

    Returns:
        CreateCategoryResponse: Созданная категория.

    Raises:
        HTTPException: Если произошла ошибка при создании категории.
    """
    try:
        category: CreateCategoryResponse = await create_category(session, category_data)
    except CategoryAlreadyExistError as e:
        raise HTTPException(400, str(e)) from e

    return category
