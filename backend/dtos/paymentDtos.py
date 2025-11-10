from pydantic import BaseModel, Field
from typing import Optional


class PaymentCreateDto(BaseModel):
    order_id: int = Field(..., example=101)
    total: float = Field(..., example=15.00)
    currency: str = Field(default="CAD")
    description: Optional[str] = Field(default="Payment")


class PaymentCaptureDto(BaseModel):
    paypal_order_id: str = Field(..., example="7SG12345ABCDEF")
    user_id: Optional[int] = None


class PaymentCancelDto(BaseModel):
    paypal_order_id: Optional[str] = None
    reason: Optional[str] = None
