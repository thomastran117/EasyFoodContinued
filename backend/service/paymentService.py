from tasks.paymentTasks import process_payment_task
from config.celeryConfig import celery_app

class PaymentService:
    def enqueue_payment(self, order_id: str, total: str, currency: str = "CAD", delay_seconds: int = 60):
        """
        Enqueue a delayed Celery task to execute the PayPal payment.
        """
        job = process_payment_task.apply_async(
            args=[order_id, total, currency],
            countdown=delay_seconds
        )
        return {"status": "queued", "task_id": job.id, "eta_seconds": delay_seconds}

    def cancel_queued_payment(self, task_id: str):
        """
        Attempt to revoke a scheduled or pending Celery task.
        """
        try:
            result = celery_app.control.revoke(task_id, terminate=False)
            return {"status": "cancelled", "task_id": task_id}
        except Exception as e:
            return {"status": "error", "error": str(e)}