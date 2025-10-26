import hashlib
import secrets
import shutil
from pathlib import Path

from fastapi import HTTPException, UploadFile
from fastapi.responses import FileResponse

BASE_UPLOAD_DIR = Path(__file__).resolve().parent.parent.parent / "uploads"
BASE_UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


class FileService:
    def __init__(self):
        self.ALLOWED_CATEGORIES = {"foods", "restaurants", "users"}
        self.ALLOWED_IMAGE_TYPES = {"jpg", "jpeg", "png", "webp"}

    def compute_file_hash(self, upload_file: UploadFile) -> str:
        """Compute SHA-256 hash of the uploaded file content."""
        hasher = hashlib.sha256()
        upload_file.file.seek(0)
        while chunk := upload_file.file.read(8192):
            hasher.update(chunk)
        upload_file.file.seek(0)
        return hasher.hexdigest()

    async def save_upload_file(
        self, upload_file: UploadFile, category: str, image_type: str
    ) -> str:
        """Save uploaded file to category folder with duplicate detection."""
        category = category.lower().strip()
        if category not in self.ALLOWED_CATEGORIES:
            raise HTTPException(status_code=400, detail=f"Invalid category: {category}")

        image_type = image_type.lower().strip(".")
        if image_type not in self.ALLOWED_IMAGE_TYPES:
            raise HTTPException(status_code=400, detail="Unsupported image type")

        category_dir = BASE_UPLOAD_DIR / category
        category_dir.mkdir(parents=True, exist_ok=True)

        file_hash = self.compute_file_hash(upload_file)
        existing = next(category_dir.glob(f"*_{file_hash}.{image_type}"), None)

        if existing:
            return str(existing.relative_to(BASE_UPLOAD_DIR.parent))

        filename = f"{category}_{file_hash}.{image_type}"
        file_path = category_dir / filename

        try:
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(upload_file.file, buffer)
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Failed to save file: {str(e)}"
            )

        return str(file_path.relative_to(BASE_UPLOAD_DIR.parent))

    def get_uploaded_file(self, category: str, filename: str):
        """Retrieve a file safely from uploads."""
        category_dir = BASE_UPLOAD_DIR / category
        if category not in self.ALLOWED_CATEGORIES or not category_dir.exists():
            raise HTTPException(status_code=404, detail="Invalid category")

        file_path = category_dir / filename
        if not file_path.exists():
            raise HTTPException(status_code=404, detail="File not found")

        return FileResponse(file_path)

    def delete_uploaded_file(self, category: str, filename: str):
        """Delete uploaded file from disk."""
        category_dir = BASE_UPLOAD_DIR / category
        if category not in self.ALLOWED_CATEGORIES or not category_dir.exists():
            raise HTTPException(status_code=404, detail="Invalid category")

        file_path = category_dir / filename
        if not file_path.exists():
            raise HTTPException(status_code=404, detail="File not found")

        try:
            file_path.unlink()
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Failed to delete file: {str(e)}"
            )

        return True
