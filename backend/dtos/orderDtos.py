from typing import List, Literal, Optional

from pydantic import BaseModel


class FoodRequest(BaseModel):
    food_id: int
    quantity: int = 1


class FulfillmentRequest(BaseModel):
    type: Literal["delivery", "pickup"]
    address: str


class PaymentRequest(BaseModel):
    type: Literal["credit", "debit"]
    name: str
    cardNumber: str
    expiry: str
    cvv: str


class CreateOrderRequest(BaseModel):
    items: List[FoodRequest]
    fulfillment: FulfillmentRequest
    notes: Optional[str] = ""
    payment: PaymentRequest


class UpdateOrderRequest(BaseModel):
    items: List[FoodRequest]
    fulfillment: Optional[FulfillmentRequest]
    notes: Optional[str] = ""
    payment: Optional[PaymentRequest]
