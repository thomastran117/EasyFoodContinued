from pydantic import BaseModel, Field
from typing import Optional


class PaymentRequest(BaseModel):
    total: str = Field(..., example="15.00")
    currency: str = Field(default="CAD")
    description: Optional[str] = Field(default="Payment")


class PaymentSuccessDto(BaseModel):
    paymentId: str
    PayerID: str


class PaymentCancelDto(BaseModel):
    token: Optional[str] = None
