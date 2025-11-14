from fastapi import APIRouter, Depends, HTTPException, status, Request
from pydantic import BaseModel, Field
from typing import Optional, List
from utilities.logger import logger

from service.orderService import OrderService
from service.paymentService import PaymentService
from schema.psql_template import OrderStatus
from dtos.orderDtos import CreateOrderDto, CancelOrderDto
from utilities.errorRaiser import (
    ServiceUnavaliableException,
    UnauthorizedException,
    raise_error,
)


class OrderController:
    def __init__(self, order_service: OrderService):
        """
        order_service: instance of AuthService (which uses PaymentService internally)
        """
        self.order_service = order_service
        self.request: Request | None = None

    async def create_order(self, payload: CreateOrderDto):
        """
        Create a new order and queue payment through Celery.
        """
        try:
            logger.info(f"[OrderController] Creating order for user {payload.user_id}")

            result = self.order_service.create_order(
                user_id=payload.user_id,
                content=payload.content,
                total=payload.total,
                fulfillment_type=payload.fulfillment_type,
                address=payload.address or "",
                notes=payload.notes,
            )

            if result.get("status") == "failed":
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Payment queue failed",
                )

            return {
                "message": "Order created successfully",
                "order_id": result["order_id"],
                "status": result["status"],
                "task_id": result.get("task_id"),
            }

        except Exception as e:
            raise_error(e)

    async def get_order(self, order_id: int):
        """
        Get details of a specific order.
        """
        try:
            result = self.order_service.get_order_content(order_id)
            if result.get("status") == "error":
                raise HTTPException(status_code=404, detail=result["message"])
            return result
        except Exception as e:
            raise_error(e)

    async def get_order_status(self, order_id: int):
        """
        Check the current status of an order.
        """
        try:
            result = self.order_service.get_order_status(order_id)
            if result.get("status") == "error":
                raise HTTPException(status_code=404, detail=result["message"])
            return result
        except Exception as e:
            raise_error(e)

    async def get_user_orders(self, user_id: int):
        """
        Get a summary list of all orders for a user.
        """
        try:
            logger.info(f"[OrderController] Fetching all orders for user {user_id}")
            return self.order_service.get_all_order_metadata(user_id)
        except Exception as e:
            raise_error(e)

    async def cancel_order(self, payload: CancelOrderDto):
        """
        Cancel an order if it's pending or queued.
        """
        try:
            result = self.order_service.cancel_order(payload.order_id)
            if result.get("status") == "error":
                raise HTTPException(status_code=400, detail=result["message"])
            return result
        except Exception as e:
            raise_error(e)
