from typing import Annotated

from database import get_async_session
from fastapi import APIRouter, Depends, HTTPException
from schemas.api.yookassa.yookassa_webhook import YookassaWebhook
from services.api.yookassa.payment_processing import payment_processing
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()


@router.post(
    "/success",
    summary="Обработка успешного платежа и начисление баллов",
    response_model=None,
    description="""
        Обрабатывает вебхук от YooKassa о подтверждённом платеже и запускает цепочку бизнес-логики:

        - Поиск пользователя по `user_platform_id` из метаданных платежа.
        - Начисление баллов (поинтов) пользователю.
        - Отправка уведомления пользователю в Telegram.
        - Обновление информации о балансах.
        - Оповещение администраторов о новом платеже.

        Эндпоинт предназначен для приёма POST-запросов от YooKassa после успешной оплаты.
        Убедитесь, что в настройках YooKassa указан корректный URL с HTTPS.
    """,
    responses={
        200: {
            "description": "Платёж успешно обработан",
            "content": {
                "application/json": {
                    "example": {"detail": "success"}
                }
            }
        },
        500: {
            "description": "Внутренняя ошибка сервера при обработке платежа",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Ошибка при обработке платежа: не удалось найти пользователя"
                    }
                }
            }
        }
    }
)
async def success(
    payload: YookassaWebhook,
    session: Annotated[AsyncSession, Depends(get_async_session)],
):
    """
    Обрабатывает успешный платёж из YooKassa и выполняет бизнес-логику.

    Вызывает сервис `payment_processing`, который:
    - находит пользователя по ID из метаданных;
    - начисляет указанное количество баллов (поинтов);
    - отправляет пользователю уведомление об успешной оплате;
    - обновляет информацию о балансах;
    - оповещает администраторов о новом платеже.

    В случае ошибки возвращает HTTP 500 с описанием исключения.

    :param payload: Данные вебхука от YooKassa в формате `YookassaWebhook`.
                    Должны содержать метаданные: user_platform_id, points_count.
    :param session: Асинхронная сессия SQLAlchemy, внедрённая через зависимость.
    :return: JSON-ответ вида `{"detail": "success"}` при успешной обработке.
    :raises HTTPException: Если произошла ошибка при обработке платежа (код 500).
    """
    try:
        await payment_processing(payload, session)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Ошибка при обработке платежа: {str(e)}"
        )

    return {"detail": "success"}
