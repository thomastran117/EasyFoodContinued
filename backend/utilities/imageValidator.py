import requests
from PIL import Image
from io import BytesIO
import io, hashlib, filetype
from fastapi import UploadFile, HTTPException
from PIL import Image, UnidentifiedImageError
import pyclamd


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


async def validate_image(file: UploadFile):
    data = await file.read()
    if len(data) > 10 * 1024 * 1024:
        raise HTTPException(413, "File too large")

    kind = filetype.guess(data)
    if not kind or kind.mime not in ["image/jpeg", "image/png"]:
        raise HTTPException(400, "Only JPG/PNG allowed")

    try:
        img = Image.open(io.BytesIO(data))
        img.load()
    except UnidentifiedImageError:
        raise HTTPException(400, "Invalid or corrupted image")

    width, height = img.size
    if width > 4096 or height > 4096 or width * height > 12_000_000:
        raise HTTPException(400, "Image dimensions too large")

    if img.mode not in ("RGB", "RGBA"):
        raise HTTPException(400, f"Unsupported color mode: {img.mode}")

    ratio = width / height
    if ratio < 0.1 or ratio > 10:
        raise HTTPException(400, "Invalid aspect ratio")

    if hasattr(img, "getexif"):
        img.info.pop("exif", None)

    hash_val = hashlib.sha256(data).hexdigest()

    file.file.seek(0)
    return {"data": data, "hash": hash_val, "width": width, "height": height}
