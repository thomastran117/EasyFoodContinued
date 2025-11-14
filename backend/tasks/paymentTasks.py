from datetime import datetime
import math

from config.celeryConfig import celery_app
from resources.database_client import get_db
from utilities.logger import logger
from schema.psql_template import Order, OrderStatus
from container.containerWorkerBootstrap import container
from service.webService import WebService

MAX_RETRIES = 5


def _retry_with_backoff(task, exc, countdown_base=10):
    retries = task.request.retries
    if retries < MAX_RETRIES:
        countdown = int(math.pow(2, retries) * countdown_base)
        logger.warning(
            f"[Celery] Task {task.name} failed (attempt {retries + 1}/{MAX_RETRIES}), "
            f"retrying in {countdown}s. Error: {exc}"
        )
        raise task.retry(exc=exc, countdown=countdown)
    else:
        logger.error(
            f"[Celery] Task {task.name} exceeded {MAX_RETRIES} retries; purging from queue."
        )
        return {"status": "purged", "error": str(exc)}


@celery_app.task(bind=True, name="cancel_payment_task", max_retries=MAX_RETRIES)
def cancel_payment_task(self, paypal_order_id: str, order_id: int):
    """
    Cancels a pending PayPal order and updates the local database record.
    """
    logger.info(f"[Celery] Attempting to cancel PayPal order {paypal_order_id}")

    try:
        web_service: WebService = container.resolve("WebService")

        token = web_service.getPaypalToken()
        result = web_service.cancelPayPalOrder(paypal_order_id, token)

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
            db.flush()

        logger.info(
            f"[Celery] Cancelled PayPal order {paypal_order_id} for Order {order_id}"
        )
        return {
            "status": "cancelled",
            "paypal_order_id": paypal_order_id,
            "result": result,
        }

    except Exception as e:
        return _retry_with_backoff(self, e)


@celery_app.task(bind=True, name="finalize_payment_task", max_retries=MAX_RETRIES)
def finalize_payment_task(self, paypal_order_id: str, order_id: int):
    """
    Captures a pending PayPal order. If capture succeeds,
    schedules process_payment_task; otherwise cancels the order.
    """
    logger.info(f"[Celery] Finalizing PayPal order {paypal_order_id}")

    try:
        web_service: WebService = container.resolve("WebService")
        capture = web_service.capturePaypalOrder(paypal_order_id)

        if capture.get("status") == "COMPLETED":
            logger.info(
                f"[Celery] PayPal order {paypal_order_id} captured successfully."
            )
            process_payment_task.apply_async(args=[order_id])
            return {"status": "captured"}

        logger.warning(f"[Celery] Capture failed for {paypal_order_id}: {capture}")
        cancel_payment_task.apply_async(args=[paypal_order_id, order_id])
        return {"status": "cancelled"}

    except Exception as e:
        logger.error(f"[Celery] Finalize failed for {paypal_order_id}: {e}")
        return _retry_with_backoff(self, e)


@celery_app.task(bind=True, name="process_payment_task", max_retries=MAX_RETRIES)
def process_payment_task(self, order_id: int):
    """
    Updates the database to mark an order as fully paid.
    """
    logger.info(f"[Celery] Marking order {order_id} as PAID.")

    try:
        with get_db() as db:
            order = db.query(Order).filter(Order.id == order_id).first()
            if not order:
                logger.error(f"[Celery] Order {order_id} not found")
                return {"status": "error"}

            order.status = OrderStatus.PAID
            order.updated_at = datetime.utcnow()
            db.flush()

        logger.info(f"[Celery] Order {order_id} finalized as PAID.")
        return {"status": "success", "order_id": order_id}

    except Exception as e:
        return _retry_with_backoff(self, e)
