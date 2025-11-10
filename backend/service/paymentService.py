import requests
from datetime import datetime
from config.envConfig import settings
from config.celeryConfig import celery_app
from resources.database_client import get_db
from schema.template import Order, OrderStatus, Payment, PaymentMethod
from utilities.logger import logger
from utilities.celeryHealthCheck import CeleryHealth


class PayPalAPI:
    def __init__(self):
        self.base_url = "https://api-m.sandbox.paypal.com"
        self.client_id = settings.paypal_client_id
        self.client_secret = settings.paypal_secret_key

    def _get_access_token(self):
        r = requests.post(
            f"{self.base_url}/v1/oauth2/token",
            auth=(self.client_id, self.client_secret),
            data={"grant_type": "client_credentials"},
        )
        r.raise_for_status()
        return r.json()["access_token"]

    def create_order(self, total: float, currency="CAD"):
        token = self._get_access_token()
        payload = {
            "intent": "CAPTURE",
            "purchase_units": [
                {"amount": {"currency_code": currency, "value": f"{total:.2f}"}}
            ],
            "application_context": {
                "return_url": f"http://localhost:8050/api/payment/capture",
                "cancel_url": f"http://localhost:8050/api/payment/cancel",
            },
        }
        r = requests.post(
            f"{self.base_url}/v2/checkout/orders",
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json",
            },
            json=payload,
        )
        r.raise_for_status()
        return r.json()

    def capture_order(self, order_id: str):
        token = self._get_access_token()
        r = requests.post(
            f"{self.base_url}/v2/checkout/orders/{order_id}/capture",
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json",
            },
        )
        r.raise_for_status()
        return r.json()

    def cancel_order(self, order_id: str, token: str):
        url = f"{self.base_url}/v2/checkout/orders/{order_id}/void"
        r = requests.post(
            url,
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json",
            },
        )
        if r.status_code == 204:
            logger.info(f"[PayPal] Order {order_id} voided successfully.")
            return {"status": "cancelled"}
        logger.warning(f"[PayPal] Cancel order failed: {r.text}")
        return {"status": "error", "response": r.text}


class PaymentService:
    """
    Orchestrates PayPal creation, capture, and Celery scheduling.
    """

    def __init__(self, db_factory=get_db):
        self.db_factory = db_factory
        self.paypal = PayPalAPI()
        self.health = CeleryHealth()
        
    def create_payment(self, order_id: int, total: float, currency="CAD"):
        try:
            if not self.health.check():
                return
            order_data = self.paypal.create_order(total, currency)
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
            capture_data = self.paypal.capture_order(paypal_order_id)

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
            token = self.paypal._get_access_token()
            result = self.paypal.cancel_order(paypal_order_id, token)

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
