import httpx

from config.envConfig import settings
from utilities.logger import logger

RECAPTCHA_SECRET = settings.google_secret_key


async def google_verify_captcha(token: str) -> bool:
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.post(
                "https://www.google.com/recaptcha/api/siteverify",
                data={
                    "secret": RECAPTCHA_SECRET,
                    "response": token,
                },
            )

        result = response.json()
        success = result.get("success", False)
        score = result.get("score", 0)

        return success and score >= 0.5

    except httpx.RequestError as e:
        logger.error(f"Recaptcha Network error: {e}")
        return False

    except Exception as e:
        logger.error(f"Recaptcha Unexpected error: {e}")
        return False
