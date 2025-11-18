import hashlib
import shutil
from pathlib import Path

from fastapi import HTTPException, UploadFile
from fastapi.responses import FileResponse

from utilities.errorRaiser import (
    AppHttpException,
    BadRequestException,
    InternalErrorException,
    NotFoundException,
)
from utilities.logger import logger

BASE_UPLOAD_DIR = Path(__file__).resolve().parent.parent.parent / "uploads"
BASE_UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


class FileService:
    ALLOWED_CATEGORIES = {"foods", "restaurants", "users"}
    ALLOWED_IMAGE_TYPES = {"jpg", "jpeg", "png", "webp"}

    def __init__(self, base_dir: Path = BASE_UPLOAD_DIR):
        self.base_dir = base_dir

    def computeFileHash(self, upload_file: UploadFile) -> str:
        """Compute SHA-256 hash of uploaded file."""
        try:
            hasher = hashlib.sha256()
            upload_file.file.seek(0)
            for chunk in iter(lambda: upload_file.file.read(8192), b""):
                hasher.update(chunk)
            upload_file.file.seek(0)
            return hasher.hexdigest()
        except AppHttpException:
            raise
        except Exception as e:
            logger.error(f"[FileService] computeFileHash failed: {e}", exc_info=True)
            raise InternalErrorException("Internal server error")

    async def handleUploadFile(self, upload_file: UploadFile, category: str) -> str:
        """Save file with hashed name (no category prefix)."""
        try:
            category = category.lower().strip()
            suffix = Path(upload_file.filename).suffix.lower().strip(".")
            if category not in self.ALLOWED_CATEGORIES:
                raise BadRequestException(f"Invalid category: {category}")
            if suffix not in self.ALLOWED_IMAGE_TYPES:
                raise BadRequestException(f"Unsupported image type: {suffix}")

            category_dir = self.base_dir / category
            category_dir.mkdir(parents=True, exist_ok=True)

            file_hash = self.computeFileHash(upload_file)
            filename = f"{file_hash}.{suffix}"
            file_path = category_dir / filename

            if file_path.exists():
                return str(file_path.relative_to(self.base_dir.parent)).replace(
                    "\\", "/"
                )

            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(upload_file.file, buffer)

            return str(file_path.relative_to(self.base_dir.parent)).replace("\\", "/")
        except AppHttpException:
            raise
        except Exception as e:
            logger.error(f"[FileService] handleUploadFile failed: {e}", exc_info=True)
            raise InternalErrorException("Internal server error")

    def getUploadFile(self, category: str, filename: str):
        """Return FileResponse if file exists."""
        try:
            file_path = self.base_dir / category / filename
            if category not in self.ALLOWED_CATEGORIES or not file_path.exists():
                raise NotFoundException(f"File '{filename}' is not found")
            return FileResponse(file_path)
        except AppHttpException:
            raise
        except Exception as e:
            logger.error(f"[FileService] getUploadFile failed: {e}", exc_info=True)
            raise InternalErrorException("Internal server error")

    def deleteUploadFile(self, category: str, filename: str):
        """Delete uploaded file."""
        try:
            file_path = self.base_dir / category / filename
            if not file_path.exists():
                raise NotFoundException(f"File '{filename}' is not found")

            file_path.unlink()
            return True
        except AppHttpException:
            raise
        except Exception as e:
            logger.error(f"[FileService] deleteUploadFile failed: {e}", exc_info=True)
            raise InternalErrorException("Internal server error")
