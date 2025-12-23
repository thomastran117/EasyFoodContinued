from datetime import datetime

import requests

from config.celeryConfig import celery_app
from config.environmentConfig import settings
from service.baseService import BaseService
from service.webService import WebService
from utilities.celeryHealthCheck import CeleryHealth
from utilities.logger import logger


class PaymentService:
    """
    Orchestrates PayPal creation, capture, and Celery scheduling.
    """

    def __init__(self, web_service: WebService):
        return
