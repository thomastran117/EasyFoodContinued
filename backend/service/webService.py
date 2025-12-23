import asyncio
import random
from typing import Callable, TypeVar

import httpx

from config.environmentConfig import settings
from utilities.logger import logger

T = TypeVar("T")


async def retry_async(
    fn: Callable[[], T],
    *,
    retries: int = 3,
    base_delay: float = 0.5,
    factor: float = 2.0,
    max_delay: float = 5.0,
    retry_on: tuple[type[Exception], ...] = (Exception,),
):
    attempt = 0

    while True:
        try:
            return await fn()
        except retry_on as e:
            attempt += 1
            if attempt > retries:
                raise

            delay = min(base_delay * (factor ** (attempt - 1)), max_delay)
            delay += random.uniform(0, 0.2)
            await asyncio.sleep(delay)


class WebService:
    """
    Unified external API service for:
      - Google reCAPTCHA
      - PayPal
    """

    def __init__(self):
        self.recaptcha_secret = settings.google_secret_key
        self.paypal_base_url = "https://api-m.sandbox.paypal.com"
        self.paypal_client_id = settings.paypal_client_id
        self.paypal_secret = settings.paypal_secret_key
        self.backend_url = settings.backend_url

        self.timeout = httpx.Timeout(5.0, connect=3.0)
        self.max_retries = 3

    def is_recaptcha_available(self) -> bool:
        return bool(self.recaptcha_secret)

    async def verifyGoogleCaptcha(self, token: str) -> bool:
        """
        Fail-open captcha verification.
        If Google is down → do NOT block users.
        """
        if not self.is_recaptcha_available():
            logger.warn("[WebService] reCAPTCHA disabled — skipping validation")
            return True

        async def op():
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                r = await client.post(
                    "https://www.google.com/recaptcha/api/siteverify",
                    data={
                        "secret": self.recaptcha_secret,
                        "response": token,
                    },
                )
                r.raise_for_status()
                return r.json()

        try:
            result = await retry_async(
                op,
                retries=self.max_retries,
                retry_on=(httpx.RequestError, httpx.HTTPStatusError),
            )

            success = result.get("success", False)
            score = result.get("score", 0.0)
            return success and score >= 0.5

        except Exception as e:
            logger.error(f"[WebService] reCAPTCHA failed — fail open: {e}")
            return True

    async def _get_paypal_token(self) -> str:
        async def op():
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                r = await client.post(
                    f"{self.paypal_base_url}/v1/oauth2/token",
                    auth=(self.paypal_client_id, self.paypal_secret),
                    data={"grant_type": "client_credentials"},
                )
                r.raise_for_status()
                return r.json()["access_token"]

        try:
            token = await retry_async(
                op,
                retries=self.max_retries,
                retry_on=(httpx.RequestError, httpx.HTTPStatusError),
            )
            logger.info("[WebService] PayPal access token retrieved")
            return token
        except Exception as e:
            logger.error(f"[WebService] PayPal token fetch failed: {e}")
            raise

    async def createPayPalOrder(self, total: float, currency: str = "CAD") -> dict:
        token = await self._get_paypal_token()

        payload = {
            "intent": "CAPTURE",
            "purchase_units": [
                {"amount": {"currency_code": currency, "value": f"{total:.2f}"}}
            ],
            "application_context": {
                "return_url": f"{self.backend_url}/payment/capture",
                "cancel_url": f"{self.backend_url}/payment/cancel",
            },
        }

        async def op():
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                r = await client.post(
                    f"{self.paypal_base_url}/v2/checkout/orders",
                    headers={"Authorization": f"Bearer {token}"},
                    json=payload,
                )
                r.raise_for_status()
                return r.json()

        try:
            result = await retry_async(
                op,
                retries=self.max_retries,
                retry_on=(httpx.RequestError, httpx.HTTPStatusError),
            )
            logger.info("[WebService] PayPal order created")
            return result
        except Exception as e:
            logger.error(f"[WebService] Failed to create PayPal order: {e}")
            raise

    async def capturePaypalOrder(self, order_id: str) -> dict:
        token = await self._get_paypal_token()

        async def op():
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                r = await client.post(
                    f"{self.paypal_base_url}/v2/checkout/orders/{order_id}/capture",
                    headers={"Authorization": f"Bearer {token}"},
                )
                r.raise_for_status()
                return r.json()

        try:
            result = await retry_async(
                op,
                retries=self.max_retries,
                retry_on=(httpx.RequestError, httpx.HTTPStatusError),
            )
            logger.info(f"[WebService] PayPal order {order_id} captured")
            return result
        except Exception as e:
            logger.error(f"[WebService] Capture failed for {order_id}: {e}")
            raise
