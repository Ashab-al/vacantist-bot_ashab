import uuid

from config import settings
from models import User
from yookassa import Payment
from yookassa.domain.models.amount import Amount
from yookassa.domain.models.confirmation.confirmation import Confirmation
from yookassa.domain.request import PaymentRequest
from yookassa.domain.response import PaymentResponse


def create_payment(amount: int, description: str, user: User, points_count: int):
    payment: PaymentResponse = Payment.create(
        generate_payment_request(
            amount=amount, description=description, user=user, points_count=points_count
        ),
        uuid.uuid4(),
    )

    return payment


def generate_payment_request(
    amount: int, description: str, user: User, points_count: int
) -> PaymentRequest:
    return PaymentRequest(
        amount={"value": amount, "currency": "RUB"},
        description=description,
        confirmation={
            "type": settings.yookassa_confirmation_type,
            "return_url": settings.yookassa_after_pay_redirect_url,
        },
        capture=True,
        metadata={
            "user_id": user.id,
            "user_platform_id": user.platform_id,
            "points_count": points_count,
        },
    )
