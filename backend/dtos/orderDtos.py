from pydantic import BaseModel, Field
from typing import Optional, List


class CreateOrderDto(BaseModel):
    user_id: int = Field(..., description="ID of the user creating the order")
    content: str = Field(..., description="Items or content of the order")
    total: float = Field(..., gt=0, description="Total price of the order")
    fulfillment_type: str = Field(
        ..., description="Type of fulfillment (pickup, delivery, etc.)"
    )
    address: Optional[str] = Field(None, description="Delivery address if applicable")
    notes: Optional[str] = Field(None, description="Optional notes for the order")


class CancelOrderDto(BaseModel):
    order_id: int = Field(..., description="Order ID to cancel")
