import paypalrestsdk
from datetime import datetime

from config.paypalConfig import init_paypal
from config.celeryConfig import celery_app
from resources.database_client import get_db
from utilities.logger import logger

from schema.template import Order, OrderStatus, Payment, PaymentMethod

init_paypal()


@celery_app.task(bind=True, name="process_payment_task", max_retries=3)
def process_payment_task(self, order_id: int, total: float, currency: str = "CAD"):
    """
    Background Celery task to execute and record a PayPal payment for an order.
    This runs in a Celery worker and updates the database upon success or failure.
    """
    logger.info(f"[Celery] Starting payment for order_id={order_id}")

    with get_db() as db:
        # 1. Load order
        order = db.query(Order).filter(Order.id == order_id).first()
        if not order:
            logger.error(f"[Celery] Order {order_id} not found")
            return {"status": "error", "error": "Order not found"}

        # 2. Skip if already paid or cancelled
        if order.status in (OrderStatus.PAID, OrderStatus.CANCELLED):
            logger.info(
                f"[Celery] Order {order_id} already {order.status.value}, skipping."
            )
            return {"status": "ignored", "order_status": order.status.value}

        try:
            order.status = OrderStatus.QUEUE
            db.commit()

            paypal_payment = paypalrestsdk.Payment(
                {
                    "intent": "sale",
                    "payer": {"payment_method": "paypal"},
                    "transactions": [
                        {
                            "amount": {"total": f"{total:.2f}", "currency": currency},
                            "description": f"Payment for order #{order_id}",
                        }
                    ],
                    "redirect_urls": {
                        "return_url": "http://localhost:8050/api/payment/success",
                        "cancel_url": "http://localhost:8050/api/payment/cancel",
                    },
                }
            )

            paypal_payment.headers = {"PayPal-Request-Id": f"order-{order_id}"}

            if paypal_payment.create():
                logger.info(
                    f"[Celery] PayPal payment created successfully: {paypal_payment.id}"
                )

                payment_entry = Payment(
                    method=PaymentMethod.PAYPAL,
                    paypal_order_id=paypal_payment.id,
                    paypal_status=paypal_payment.state,
                    order_id=order.id,
                    created_at=datetime.utcnow(),
                )
                db.add(payment_entry)
                db.flush()

                if paypal_payment.state in ("approved", "created"):
                    order.status = OrderStatus.PAID
                    order.payment_id = payment_entry.id
                    db.commit()
                    logger.info(f"[Celery] Order {order.id} marked as PAID.")
                    return {
                        "status": "paid",
                        "order_id": order.id,
                        "payment_id": payment_entry.id,
                        "paypal_id": paypal_payment.id,
                    }
                else:
                    order.status = OrderStatus.FAILED
                    db.commit()
                    logger.warning(
                        f"[Celery] Payment state not approved: {paypal_payment.state}"
                    )
                    return {
                        "status": "failed",
                        "paypal_status": paypal_payment.state,
                    }

            else:
                logger.error(
                    f"[Celery] PayPal payment creation failed: {paypal_payment.error}"
                )
                order.status = OrderStatus.FAILED
                db.commit()
                return {"status": "failed", "error": paypal_payment.error}

        except Exception as e:
            logger.error(f"[Celery] Exception while processing order {order_id}: {e}")
            db.rollback()
            order.status = OrderStatus.FAILED
            db.commit()

            raise self.retry(exc=e, countdown=10)
