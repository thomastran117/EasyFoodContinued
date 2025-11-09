# service/paymentService.py
import paypalrestsdk
from datetime import datetime

from tasks.paymentTasks import process_payment_task
from config.celeryConfig import celery_app
from utilities.logger import logger
from resources.database_client import get_db
from schema.template import Order, OrderStatus, Payment, PaymentMethod
from config.paypalConfig import init_paypal

init_paypal()


class PaymentService:
    """
    Handles PayPal payment orchestration and Celery queuing.
    """

    def __init__(self, db_factory=get_db):
        self.db_factory = db_factory

    def enqueue_payment(
        self,
        order_id: int,
        user_id: int,
        total: float,
        currency: str = "CAD",
        delay_seconds: int = 5,
    ):
        try:
            with self.db_factory() as db:
                order = db.query(Order).filter(Order.id == order_id).first()
                if not order:
                    return {"status": "error", "error": "Order not found"}

                if order.status in [OrderStatus.QUEUE, OrderStatus.PAID]:
                    return {
                        "status": "ignored",
                        "message": f"Order {order_id} already {order.status.value}",
                        "task_id": order.task_id,
                    }

                job = process_payment_task.apply_async(
                    args=[order_id, total, currency],
                    countdown=delay_seconds,
                )

                order.status = OrderStatus.QUEUE
                order.task_id = job.id
                db.commit()

                logger.info(
                    f"[PaymentService] Queued Celery task {job.id} for order {order_id}"
                )
                return {
                    "status": "queued",
                    "task_id": job.id,
                    "eta_seconds": delay_seconds,
                }

        except Exception as e:
            logger.error(f"[PaymentService] Failed to enqueue payment: {e}")
            return {"status": "error", "error": str(e)}

    def execute_payment(self, paymentId: str, PayerID: str):
        """
        Completes PayPal payment execution once user approves it.
        """
        try:
            logger.info(f"[PayPal] Executing payment for paymentId={paymentId}")

            payment = paypalrestsdk.Payment.find(paymentId)
            if not payment:
                return {"status": "error", "message": "Payment not found in PayPal"}

            if payment.execute({"payer_id": PayerID}):
                with self.db_factory() as db:
                    record = (
                        db.query(Payment)
                        .filter(Payment.paypal_order_id == paymentId)
                        .first()
                    )
                    if not record:
                        return {
                            "status": "error",
                            "message": "Payment record not found",
                        }

                    order = db.query(Order).filter(Order.id == record.order_id).first()
                    if not order:
                        return {"status": "error", "message": "Order not found"}

                    order.status = OrderStatus.PAID
                    record.paypal_status = payment.state
                    record.paypal_capture_id = (
                        payment.transactions[0].related_resources[0].sale.id
                        if payment.transactions
                        else None
                    )
                    db.commit()

                    logger.info(f"[PayPal] Order {order.id} marked as PAID (executed).")

                return {
                    "status": "success",
                    "order_id": order.id,
                    "paypal_status": payment.state,
                }

            else:
                logger.error(f"[PayPal] Execute failed: {payment.error}")
                return {"status": "error", "message": str(payment.error)}

        except Exception as e:
            logger.error(f"[PayPal] Exception during execute_payment: {e}")
            return {"status": "error", "message": str(e)}

    def cancel_queued_payment(self, task_id: str):
        try:
            celery_app.control.revoke(task_id, terminate=False)
            logger.info(f"[PaymentService] Revoked Celery task {task_id}")
            return {"status": "cancelled", "task_id": task_id}
        except Exception as e:
            logger.error(f"[PaymentService] Failed to revoke task {task_id}: {e}")
            return {"status": "error", "error": str(e)}

    def get_payment_status(self, task_id: str):
        async_result = celery_app.AsyncResult(task_id)
        return {
            "task_id": task_id,
            "status": async_result.status,
            "result": async_result.result,
        }
