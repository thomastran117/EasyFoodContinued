from service.fileService import FileService
from utilities.errorRaiser import AppHttpException, raise_error
from utilities.logger import logger


class FileController:
    def __init__(self, file_service: FileService):
        self.file_service = file_service

    async def getUploadedFile(self, category: str, filename: str):
        """Fetch a file by category and filename."""
        try:
            return self.file_service.getUploadFile(category, filename)
        except AppHttpException as e:
            raise_error(e)
        except Exception as e:
            logger.error(f"[FileController] getUploadedFile failed: {e}")
            raise_error(e)
