import requests
from datetime import datetime
from config.environmentConfig import settings
from config.celeryConfig import celery_app
from resources.database_client import get_db
from schema.psql_template import Order, OrderStatus, Payment, PaymentMethod
from utilities.logger import logger
from utilities.celeryHealthCheck import CeleryHealth
from service.webService import WebService


class PaymentService:
    """
    Orchestrates PayPal creation, capture, and Celery scheduling.
    """

    def __init__(self, web_service: WebService, db_factory=get_db):
        self.db_factory = db_factory
        self.web_service = web_service
        self.health = CeleryHealth()

    def create_payment(self, order_id: int, total: float, currency="CAD"):
        try:
            if not self.health.check():
                return
            order_data = self.web_service.createPayPalOrder(total, currency)
            paypal_order_id = order_data["id"]

            with self.db_factory() as db:
                order = db.query(Order).filter(Order.id == order_id).first()
                if not order:
                    return {"status": "error", "message": "Order not found"}

                payment_entry = Payment(
                    method=PaymentMethod.PAYPAL,
                    paypal_order_id=paypal_order_id,
                    paypal_status="CREATED",
                    order_id=order.id,
                    created_at=datetime.utcnow(),
                )
                db.add(payment_entry)
                order.status = OrderStatus.QUEUE
                db.commit()

            approval_link = next(
                (l["href"] for l in order_data["links"] if l["rel"] == "approve"), None
            )

            finalize_job = celery_app.send_task(
                "finalize_payment_task",
                args=[paypal_order_id, order_id],
                countdown=300,
            )

            logger.info(
                f"[PaymentService] Queued finalize task {finalize_job.id} for order {order_id}"
            )

            return {
                "status": "created",
                "paypal_order_id": paypal_order_id,
                "approval_url": approval_link,
                "finalize_task_id": finalize_job.id,
            }

        except Exception as e:
            logger.error(f"[PayPal] Create payment failed: {e}")
            return {"status": "error", "message": str(e)}

    def capture_payment(self, paypal_order_id: str):
        try:
            if not self.health.check():
                return

            logger.info(f"[PayPal] Capturing order {paypal_order_id}")
            capture_data = self.web_service.capturePaypalOrder(paypal_order_id)

            with self.db_factory() as db:
                payment = (
                    db.query(Payment)
                    .filter(Payment.paypal_order_id == paypal_order_id)
                    .first()
                )
                if not payment:
                    return {"status": "error", "message": "Payment record not found"}

                order = db.query(Order).filter(Order.id == payment.order_id).first()
                if not order:
                    return {"status": "error", "message": "Order not found"}

                order.status = OrderStatus.PAID
                payment.paypal_status = "COMPLETED"
                db.commit()

            # revoke any scheduled finalizer (optional)
            # celery_app.control.revoke(order.finalize_task_id, terminate=False)

            celery_app.send_task("process_payment_task", args=[order.id], countdown=5)
            return {"status": "success", "paypal_status": "COMPLETED"}

        except Exception as e:
            logger.error(f"[PayPal] Capture failed: {e}")
            return {"status": "error", "message": str(e)}

    def cancel_user_payment(self, paypal_order_id: str):
        try:
            if not self.health.check():
                return

            logger.info(f"[PayPal] User requested cancel for {paypal_order_id}")
            token = self.web_service.getPaypalToken()
            result = self.web_service.cancelPayPalOrder(paypal_order_id, token)

            with self.db_factory() as db:
                payment = (
                    db.query(Payment)
                    .filter(Payment.paypal_order_id == paypal_order_id)
                    .first()
                )
                if not payment:
                    return {"status": "error", "message": "Payment record not found"}

                order = db.query(Order).filter(Order.id == payment.order_id).first()
                if not order:
                    return {"status": "error", "message": "Order not found"}

                order.status = OrderStatus.CANCELLED
                db.commit()

            return {
                "status": "cancelled",
                "paypal_order_id": paypal_order_id,
                "result": result,
            }

        except Exception as e:
            logger.error(f"[PayPal] User cancel failed: {e}")
            return {"status": "error", "message": str(e)}

    def view_queue(self):
        if not self.health.check():
            return
        insp = celery_app.control.inspect()
        try:
            snapshot = {
                "active": insp.active() or {},
                "reserved": insp.reserved() or {},
                "scheduled": insp.scheduled() or {},
                "revoked": insp.revoked() or {},
            }

            def _clean(entries):
                if not entries:
                    return []
                cleaned = []
                for e in entries:
                    cleaned.append(
                        {
                            "id": e.get("id"),
                            "name": e.get("name"),
                            "args": e.get("args"),
                            "eta": e.get("eta"),
                            "state": e.get("state", "queued"),
                        }
                    )
                return cleaned

            queues = {}
            for key, val in snapshot.items():
                queues[key] = _clean(next(iter(val.values()), []))

            return {"status": "success", "queues": queues}
        except Exception as e:
            logger.error(f"[Celery] Failed to inspect queue: {e}")
            return {"status": "error", "message": str(e)}

    def clear_queue(self):
        """
        Purges all messages from every Celery queue.
        Use with caution — this deletes all pending tasks immediately.
        """
        try:
            if not self.health.check():
                return
            purged = celery_app.control.purge()
            logger.warning(f"[Celery] Purged {purged} tasks from all queues.")
            return {"status": "success", "purged": purged}
        except Exception as e:
            logger.error(f"[Celery] Failed to purge Celery queues: {e}")
            return {"status": "error", "message": str(e)}
