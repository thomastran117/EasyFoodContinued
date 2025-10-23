import hashlib
import io
from io import BytesIO

import filetype
import pyclamd
import requests
from fastapi import HTTPException, UploadFile
from PIL import Image, UnidentifiedImageError


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
