from typing import Optional

from pydantic import BaseModel


class PaymentAmount(BaseModel):
    value: str
    currency: str


class PaymentMetadata(BaseModel):
    points_count: str
    user_platform_id: str
    user_id: str


class PaymentObject(BaseModel):
    id: str
    status: str
    amount: PaymentAmount
    income_amount: Optional[PaymentAmount] = None
    description: Optional[str] = None
    metadata: PaymentMetadata
    paid: bool


class YookassaWebhook(BaseModel):
    event: str
    type: str
    object: PaymentObject
