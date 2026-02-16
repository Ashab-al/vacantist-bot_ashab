from lib.tg.common import jinja_render
from models import User
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.api.yookassa.yookassa_webhook import YookassaWebhook
from services.tg.user.find_user_by_platform_id import find_user_by_platform_id
from bot.create_bot import bot
from services.tg.admin_alert import admin_alert_mailing_payments_info
from services.tg.point.show_points_info import show_points_info_for_api


async def payment_processing(
    payload: YookassaWebhook,
    db: AsyncSession
) -> None:
    user_platform_id: int = int(payload.object.metadata.user_platform_id)
    await _find_and_update_user_points(payload, db, user_platform_id)
    await _admin_alert_mailing_payments_info(
        payload,
        db,
        user_platform_id
    )
    await show_points_info_for_api(bot, db, user_platform_id)
    await _notify_user(payload)

async def _notify_user(payload):
    text = await jinja_render(
        "pre_checkout_query/success_payment", {"points": int(payload.object.metadata.points_count)}
    )

    await bot.send_message(
        chat_id=payload.object.metadata.user_platform_id,
        text=text
    )

async def _find_and_update_user_points(
    payload: YookassaWebhook,
    db: AsyncSession,
    user_platform_id: int
) -> None:
    user: User = await find_user_by_platform_id(
        db,
        user_platform_id
    )
    user.point += int(payload.object.metadata.points_count)

    db.add(user)
    await db.flush()
    await db.commit()

async def _admin_alert_mailing_payments_info(
    payload: YookassaWebhook,
    db: AsyncSession,
    user_platform_id: int
):
    user: User = await find_user_by_platform_id(
        db,
        user_platform_id
    )
    await admin_alert_mailing_payments_info(
        bot=bot,
        text=await jinja_render(
            "payment_info_for_admin_ru_card",
            {
                "name": user.first_name,
                "points": payload.object.metadata.points_count,
                "amount": payload.object.amount.value,
                "currency": payload.object.amount.currency
            },
        ),
    )