import httpx
import requests

from config.environmentConfig import settings
from utilities.errorRaiser import AppHttpException, InternalErrorException
from utilities.logger import logger


class WebService:
    def __init__(self):
        """Unified external API service for Google reCAPTCHA and PayPal."""
        self.RECAPTCHA_SECRET = settings.google_secret_key
        self.paypal_base_url = "https://api-m.sandbox.paypal.com"
        self.paypal_client_id = settings.paypal_client_id
        self.paypal_secret_key = settings.paypal_secret_key
        self.backend_url = "http://localhost:8040/api"

    def isRecaptchaAvaliable(self) -> bool:
        return self.RECAPTCHA_SECRET is not None

    async def verifyGoogleCaptcha(self, token: str) -> bool:
        """Verify Google reCAPTCHA token asynchronously."""
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.post(
                    "https://www.google.com/recaptcha/api/siteverify",
                    data={
                        "secret": self.RECAPTCHA_SECRET,
                        "response": token,
                    },
                )

            result = response.json()
            success = result.get("success", False)
            score = result.get("score", 0)

            return success and score >= 0.5

        except httpx.RequestError as e:
            logger.error(f"[WebService] Recaptcha network error: {e}")
            return False
        except Exception as e:
            logger.error(f"[WebService] Recaptcha unexpected error: {e}")
            return False

    def getPaypalToken(self) -> str:
        """Retrieve PayPal OAuth2 access token."""
        try:
            r = requests.post(
                f"{self.paypal_base_url}/v1/oauth2/token",
                auth=(self.paypal_client_id, self.paypal_secret_key),
                data={"grant_type": "client_credentials"},
            )
            r.raise_for_status()
            token = r.json()["access_token"]
            logger.info("[WebService] PayPal access token retrieved successfully.")
            return token
        except requests.RequestException as e:
            logger.error(f"[WebService] Failed to get PayPal token: {e}")
            raise

    def createPayPalOrder(self, total: float, currency: str = "CAD") -> dict:
        """Create a new PayPal order."""
        try:
            token = self.getPaypalToken()
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

            r = requests.post(
                f"{self.paypal_base_url}/v2/checkout/orders",
                headers={
                    "Authorization": f"Bearer {token}",
                    "Content-Type": "application/json",
                },
                json=payload,
            )
            r.raise_for_status()
            logger.info("[WebService] PayPal order created successfully.")
            return r.json()

        except requests.RequestException as e:
            logger.error(f"[WebService] Failed to create PayPal order: {e}")
            raise

    def capturePaypalOrder(self, order_id: str) -> dict:
        """Capture a PayPal order."""
        try:
            token = self.getPaypalToken()
            r = requests.post(
                f"{self.paypal_base_url}/v2/checkout/orders/{order_id}/capture",
                headers={
                    "Authorization": f"Bearer {token}",
                    "Content-Type": "application/json",
                },
            )
            r.raise_for_status()
            logger.info(f"[WebService] PayPal order {order_id} captured successfully.")
            return r.json()
        except requests.RequestException as e:
            logger.error(f"[WebService] Failed to capture PayPal order {order_id}: {e}")
            raise

    def cancelPayPalOrder(self, order_id: str, token: str) -> dict:
        """Cancel a PayPal order."""
        try:
            url = f"{self.paypal_base_url}/v2/checkout/orders/{order_id}/void"
            r = requests.post(
                url,
                headers={
                    "Authorization": f"Bearer {token}",
                    "Content-Type": "application/json",
                },
            )
            if r.status_code == 204:
                logger.info(
                    f"[WebService] PayPal order {order_id} voided successfully."
                )
                return {"status": "cancelled"}
            logger.warning(f"[WebService] Cancel PayPal order failed: {r.text}")
            return {"status": "error", "response": r.text}
        except requests.RequestException as e:
            logger.error(f"[WebService] Failed to cancel PayPal order {order_id}: {e}")
            raise
