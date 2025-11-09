from fastapi import HTTPException
from utilities.logger import logger
from service.paymentService import PaymentService


class PaymentController:
    """
    Controller responsible for handling PayPal success/cancel routes.
    Delegates business logic to PaymentService.
    """

    def __init__(self):
        self.payment_service = PaymentService()

    def payment_success(self, paymentId: str, PayerID: str):
        """
        Called by PayPal after user approves payment.
        Completes the transaction and updates DB.
        """
        try:
            logger.info(
                f"[PayPalController] Processing success for paymentId={paymentId}"
            )
            result = self.payment_service.execute_payment(paymentId, PayerID)

            if result.get("status") != "success":
                raise HTTPException(status_code=400, detail=result)

            return result
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"[PayPalController] Exception: {e}")
            raise HTTPException(status_code=500, detail=str(e))

    def payment_cancel(self):
        """
        Called when user cancels the PayPal payment.
        """
        return {"status": "cancelled", "message": "Payment was cancelled by the user"}
