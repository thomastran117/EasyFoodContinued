import requests
from PIL import Image
from io import BytesIO


def is_valid_image_url(url: str) -> bool:

    return True
    try:
        response = requests.get(url, timeout=5, stream=True, allow_redirects=True)

        if response.status_code != 200:
            return False

        content_type = response.headers.get("Content-Type", "")
        if not content_type.startswith("image/"):
            return False

        image = Image.open(BytesIO(response.content))
        image.verify()

        return True
    except Exception as e:
        print(f"Validation failed: {e}")
        return False
