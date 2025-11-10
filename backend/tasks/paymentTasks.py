from datetime import datetime
from config.celeryConfig import celery_app
from resources.database_client import get_db
from utilities.logger import logger
from schema.template import Order, OrderStatus
from service.paymentService import PayPalAPI


@celery_app.task(bind=True, name="cancel_payment_task", max_retries=1)
def cancel_payment_task(self, paypal_order_id: str, order_id: int):
    """Cancels (voids) a PayPal order if user cancels or timeout expires."""
    logger.info(f"[Celery] Attempting to cancel PayPal order {paypal_order_id}")
    paypal_api = PayPalAPI()

    try:
        token = paypal_api._get_access_token()
        result = paypal_api.cancel_order(paypal_order_id, token)

        with get_db() as db:
            order = db.query(Order).filter(Order.id == order_id).first()
            if not order:
                logger.error(f"[Celery] Order {order_id} not found")
                return {"status": "error"}

            if order.status == OrderStatus.PAID:
                logger.info(f"[Celery] Order {order_id} already paid; skipping cancel.")
                return {"status": "skipped"}

            order.status = OrderStatus.CANCELLED
            order.updated_at = datetime.utcnow()
            order_id_val = order.id

        logger.info(
            f"[Celery] Cancelled PayPal order {paypal_order_id} (Order {order_id_val})"
        )
        return {
            "status": "cancelled",
            "paypal_order_id": paypal_order_id,
            "result": result,
        }

    except Exception as e:
        logger.error(f"[Celery] Cancel task failed for {paypal_order_id}: {e}")
        return {"status": "error", "error": str(e)}


@celery_app.task(bind=True, name="finalize_payment_task", max_retries=1)
def finalize_payment_task(self, paypal_order_id: str, order_id: int):
    """Automatically finalizes PayPal order if user did not cancel in grace period."""
    logger.info(f"[Celery] Finalizing PayPal order {paypal_order_id}")
    paypal_api = PayPalAPI()

    try:
        capture = paypal_api.capture_order(paypal_order_id)

        if capture.get("status") == "COMPLETED":
            logger.info(
                f"[Celery] PayPal order {paypal_order_id} captured successfully."
            )
            process_payment_task.apply_async(args=[order_id])
            return {"status": "captured"}

        logger.warning(f"[Celery] Capture failed: {capture}")
        cancel_payment_task.apply_async(args=[paypal_order_id, order_id])
        return {"status": "cancelled"}

    except Exception as e:
        logger.error(f"[Celery] Finalize failed for {paypal_order_id}: {e}")
        cancel_payment_task.apply_async(args=[paypal_order_id, order_id])
        return {"status": "error", "error": str(e)}


@celery_app.task(bind=True, name="process_payment_task", max_retries=3)
def process_payment_task(self, order_id: int):
    """Post-capture task — updates DB and marks order as PAID."""
    try:
        with get_db() as db:
            order = db.query(Order).filter(Order.id == order_id).first()
            if not order:
                logger.error(f"[Celery] Order {order_id} not found")
                return {"status": "error"}

            order.status = OrderStatus.PAID
            order.updated_at = datetime.utcnow()
            db.flush()
            order_id_val = order.id

        logger.info(f"[Celery] Order {order_id_val} finalized as PAID.")
        return {"status": "success", "order_id": order_id_val}

    except Exception as e:
        logger.error(f"[Celery] Post-payment failed for order {order_id}: {e}")
        raise self.retry(exc=e, countdown=10)
