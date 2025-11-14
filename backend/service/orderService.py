from datetime import datetime
from sqlalchemy import select, update

from resources.database_client import get_db
from schema.psql_template import Order, OrderStatus
from service.paymentService import PaymentService
from utilities.logger import logger


class OrderService:
    """
    Handles all order-related logic, including creating, retrieving,
    and cancelling orders, and delegating payments to PaymentService.
    """

    def __init__(self, payment_service: PaymentService, db_factory=get_db):
        self.payment_service = payment_service
        self.db_factory = db_factory

    def create_order(
        self,
        user_id: int,
        content: str,
        total: float,
        fulfillment_type: str,
        address: str,
        notes: str | None = None,
    ):
        """
        1. Create a new Order in the database.
        2. Queue the payment via PaymentService (Celery).
        3. Update the order with task_id and QUEUE status.
        """
        with self.db_factory() as db:
            # 1. Create the order
            order = Order(
                user_id=user_id,
                content=content,
                total=total,
                notes=notes or "",
                address=address,
                fulfillment_type=fulfillment_type,
                status=OrderStatus.PENDING,
                created_at=datetime.utcnow(),
            )
            db.add(order)
            db.commit()
            db.refresh(order)

            logger.info(f"[OrderService] Created order {order.id} for user {user_id}")

            payment_result = self.payment_service.enqueue_payment(
                order.id, user_id, total
            )

            if payment_result.get("status") == "queued":
                order.status = OrderStatus.QUEUE
                order.task_id = payment_result["task_id"]
                db.commit()
                logger.info(
                    f"[OrderService] Order {order.id} queued for payment (task_id={order.task_id})"
                )
            else:
                order.status = OrderStatus.FAILED
                db.commit()
                logger.error(
                    f"[OrderService] Failed to queue payment for order {order.id}: {payment_result}"
                )

            return {
                "order_id": order.id,
                "status": order.status.value,
                "task_id": order.task_id,
            }

    def get_order_content(self, order_id: int):
        with self.db_factory() as db:
            result = db.execute(select(Order).where(Order.id == order_id))
            order = result.scalar_one_or_none()
            if not order:
                return {"status": "error", "message": "Order not found."}
            return {
                "order_id": order.id,
                "content": order.content,
                "total": order.total,
                "notes": order.notes,
            }

    def get_order_status(self, order_id: int):
        with self.db_factory() as db:
            result = db.execute(select(Order).where(Order.id == order_id))
            order = result.scalar_one_or_none()
            if not order:
                return {"status": "error", "message": "Order not found."}

            payment_state = None
            if order.task_id:
                payment_state = self.payment_service.get_payment_status(order.task_id)

            return {
                "order_id": order.id,
                "status": order.status.value if order.status else "unknown",
                "task_id": order.task_id,
                "payment_id": order.payment_id,
                "payment_task": payment_state,
            }

    def get_all_order_metadata(self, user_id: int):
        with self.db_factory() as db:
            result = db.execute(select(Order).where(Order.user_id == user_id))
            orders = result.scalars().all()
            return [
                {
                    "order_id": o.id,
                    "status": o.status.value,
                    "total": o.total,
                    "created_at": o.created_at,
                }
                for o in orders
            ]

    def cancel_order(self, order_id: int):
        """
        Cancel an order if it's still pending or queued.
        Also attempts to cancel the Celery task if not yet executed.
        """
        with self.db_factory() as db:
            result = db.execute(select(Order).where(Order.id == order_id))
            order = result.scalar_one_or_none()
            if not order:
                return {"status": "error", "message": "Order not found."}

            if order.status in (OrderStatus.PAID, OrderStatus.FAILED):
                return {
                    "status": "error",
                    "message": "Cannot cancel a processed order.",
                }

            if order.task_id:
                self.payment_service.cancel_queued_payment(order.task_id)

            order.status = OrderStatus.CANCELLED
            db.commit()

            logger.info(f"[OrderService] Order {order_id} cancelled successfully.")
            return {"status": "cancelled", "order_id": order_id}
