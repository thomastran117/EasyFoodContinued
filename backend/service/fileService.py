import secrets
import shutil
from pathlib import Path
from fastapi import UploadFile, HTTPException
from fastapi.responses import FileResponse

BASE_UPLOAD_DIR = Path(__file__).resolve().parent.parent.parent / "uploads"
BASE_UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

ALLOWED_CATEGORIES = {"foods", "restaurants", "users"}
ALLOWED_IMAGE_TYPES = {"jpg", "jpeg", "png", "webp"}


async def save_upload_file(
    upload_file: UploadFile, category: str, image_type: str
) -> str:
    """Save uploaded file to category folder with secure random name."""
    category = category.lower().strip()
    if category not in ALLOWED_CATEGORIES:
        raise HTTPException(status_code=400, detail=f"Invalid category: {category}")

    image_type = image_type.lower().strip(".")
    if image_type not in ALLOWED_IMAGE_TYPES:
        raise HTTPException(status_code=400, detail="Unsupported image type")

    category_dir = BASE_UPLOAD_DIR / category
    category_dir.mkdir(parents=True, exist_ok=True)

    random_hex = secrets.token_hex(64)
    filename = f"{category}_{random_hex}.{image_type}"
    file_path = category_dir / filename

    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(upload_file.file, buffer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save file: {str(e)}")

    return str(file_path.relative_to(BASE_UPLOAD_DIR.parent))


def get_uploaded_file(category: str, filename: str):
    category_dir = BASE_UPLOAD_DIR / category
    if category not in ALLOWED_CATEGORIES or not category_dir.exists():
        raise HTTPException(status_code=404, detail="Invalid category")

    file_path = category_dir / filename
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")

    return FileResponse(file_path)


def delete_uploaded_file(category: str, filename: str):
    category_dir = BASE_UPLOAD_DIR / category
    if category not in ALLOWED_CATEGORIES or not category_dir.exists():
        raise HTTPException(status_code=404, detail="Invalid category")

    file_path = category_dir / filename
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")

    try:
        file_path.unlink()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete file: {str(e)}")

    return True
