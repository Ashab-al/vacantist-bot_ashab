from typing import Annotated

from database import get_async_session
from fastapi import APIRouter, Depends, HTTPException
from schemas.api.yookassa.yookassa_webhook import YookassaWebhook
from services.api.yookassa.payment_processing import payment_processing
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()


@router.post(
    "/success",
    summary="Обработка платежа и зачисление поинтов пользователю",
    response_model=None,
)
async def success(
    payload: YookassaWebhook,
    session: Annotated[AsyncSession, Depends(get_async_session)],
):
    """
    Обработка платежа и зачисление поинтов пользователю.
    """
    try:
        await payment_processing(payload, session)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Ошибка при обработке платежа: {str(e)}"
        )

    return {"detail": "success"}
