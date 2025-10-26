import hashlib
import secrets
import shutil
from pathlib import Path
from fastapi import HTTPException, UploadFile
from fastapi.responses import FileResponse

BASE_UPLOAD_DIR = Path(__file__).resolve().parent.parent.parent / "uploads"
BASE_UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


class FileService:
    ALLOWED_CATEGORIES = {"foods", "restaurants", "users"}
    ALLOWED_IMAGE_TYPES = {"jpg", "jpeg", "png", "webp"}

    def __init__(self, base_dir: Path = BASE_UPLOAD_DIR):
        self.base_dir = base_dir

    def compute_file_hash(self, upload_file: UploadFile) -> str:
        """Compute SHA-256 hash of uploaded file."""
        hasher = hashlib.sha256()
        upload_file.file.seek(0)
        for chunk in iter(lambda: upload_file.file.read(8192), b""):
            hasher.update(chunk)
        upload_file.file.seek(0)
        return hasher.hexdigest()

    async def save_upload_file(self, upload_file: UploadFile, category: str) -> str:
        """Save uploaded file with hashed filename under a category."""
        category = category.lower().strip()
        suffix = Path(upload_file.filename).suffix.lower().strip(".")
        if category not in self.ALLOWED_CATEGORIES:
            raise HTTPException(400, f"Invalid category: {category}")
        if suffix not in self.ALLOWED_IMAGE_TYPES:
            raise HTTPException(400, f"Unsupported image type: {suffix}")

        category_dir = self.base_dir / category
        category_dir.mkdir(parents=True, exist_ok=True)

        file_hash = self.compute_file_hash(upload_file)
        existing = next(category_dir.glob(f"*_{file_hash}.{suffix}"), None)
        if existing:
            return str(existing.relative_to(self.base_dir.parent))

        filename = f"{category}_{file_hash}.{suffix}"
        file_path = category_dir / filename

        try:
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(upload_file.file, buffer)
        except Exception as e:
            raise HTTPException(500, f"Failed to save file: {e}")

        return str(file_path.relative_to(self.base_dir.parent))

    def get_uploaded_file(self, category: str, filename: str):
        """Return FileResponse if file exists."""
        file_path = self.base_dir / category / filename
        if category not in self.ALLOWED_CATEGORIES or not file_path.exists():
            raise HTTPException(404, "File not found")
        return FileResponse(file_path)

    def delete_uploaded_file(self, category: str, filename: str):
        """Delete uploaded file."""
        file_path = self.base_dir / category / filename
        if not file_path.exists():
            raise HTTPException(404, "File not found")

        try:
            file_path.unlink()
        except Exception as e:
            raise HTTPException(500, f"Failed to delete file: {e}")
        return True
