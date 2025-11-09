from celery import Celery
from config.envConfig import settings

BROKER_URL = settings.celery_broker_url
RESULT_BACKEND = settings.celery_result_backend

celery_app = Celery(
    "easyfood_payments",
    broker=BROKER_URL,
    backend=RESULT_BACKEND,
)

celery_app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="America/Toronto",
    enable_utc=True,
)
