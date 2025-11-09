import paypalrestsdk
from config.paypalConfig import init_paypal
from config.celeryConfig import celery_app
from utilities.logger import logger

init_paypal()

@celery_app.task(bind=True, name="process_payment_task")
def process_payment_task(self, order_id: str, total: str, currency: str = "CAD"):
    """
    Background Celery task to execute a PayPal payment.
    """
    try:
        payment = paypalrestsdk.Payment({
            "intent": "sale",
            "payer": {"payment_method": "paypal"},
            "transactions": [{
                "amount": {"total": total, "currency": currency},
                "description": f"Order {order_id}",
            }],
        })

        if payment.create():
            logger.info(f"[Celery] Payment successful for {order_id}: {payment.id}")
            return {"status": "success", "payment_id": payment.id}
        else:
            logger.error(f"[Celery] Payment failed: {payment.error}")
            return {"status": "error", "error": payment.error}
    except Exception as e:
        logger.error(f"[Celery] Exception: {str(e)}")
        raise self.retry(exc=e, countdown=10, max_retries=3)