import paypalrestsdk
from config.envConfig import settings

def init_paypal():
    paypalrestsdk.configure(
        {
            "mode": settings.paypal_mode,
            "client_id": settings.paypal_client_id,
            "client_secret": settings.paypal_secret_key,
        }
    )
