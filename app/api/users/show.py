from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_async_session
from schemas.api.users.show.response import ShowUserResponse
from schemas.api.users.show.request import ShowUserRequest
from typing import Annotated
from services.api.user.find_user_by_id import find_user_by_id


router = APIRouter()

@router.get(
    '/{id}',
    summary='Получить пользователя по id',
    description='Возвращает пользователя по id',
    response_model=ShowUserResponse
)
async def show(
    session: Annotated[AsyncSession, Depends(get_async_session)],
    user_id: Annotated[ShowUserRequest, Path()]
):
    """
    Получить пользователя по идентификатору.

    Эндпоинт ищет пользователя в базе данных по его уникальному `id` 
    и возвращает информацию о нём.

    Args:
        session (AsyncSession): Асинхронная сессия SQLAlchemy для работы с базой данных.
        user_id (ShowUserRequest): Идентификатор пользователя для поиска.

    Raises:
        HTTPException: Возвращает ошибку 400, если пользователь с указанным ID не найден.

    Returns:
        ShowUserResponse: Данные найденного пользователя.
    """
    try:
        user = await find_user_by_id(
            session, 
            user_id
        )
    except ValueError as e:
        raise HTTPException(400, str(e))

    return user