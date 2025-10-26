from fastapi import HTTPException
from fastapi.responses import FileResponse
from service.fileService import FileService
from utilities.errorRaiser import raise_error


class FileController:
    def __init__(self, file_service: FileService):
        self.file_service = file_service

    async def get_file(self, category: str, filename: str):
        """Fetch a file by category and filename."""
        try:
            return self.file_service.get_uploaded_file(category, filename)
        except Exception as e:
            raise_error(e)
