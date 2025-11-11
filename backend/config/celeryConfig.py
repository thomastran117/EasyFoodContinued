import os
import sys
from celery import Celery
from config.environmentConfig import settings

current_dir = os.path.dirname(os.path.abspath(__file__))
backend_root = os.path.abspath(os.path.join(current_dir, ".."))
if backend_root not in sys.path:
    sys.path.insert(0, backend_root)

try:
    import tasks
except ImportError:
    raise RuntimeError(f"Cannot import tasks from {backend_root}")

BROKER_URL = settings.celery_broker_url
RESULT_BACKEND = settings.celery_result_backend

celery_app = Celery(
    "easyfood_payments",
    broker=BROKER_URL,
    backend=RESULT_BACKEND,
    include=["tasks.paymentTasks"],
)

celery_app.autodiscover_tasks(["tasks"])

celery_app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="America/Toronto",
    enable_utc=True,
)
