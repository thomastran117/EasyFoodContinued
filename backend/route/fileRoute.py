from fastapi import APIRouter, Depends, Request

from controller.fileController import FileController
from utilities.errorRaiser import raise_error
from utilities.logger import logger

fileRouter = APIRouter(tags=["File"])


async def get_file_controller(request: Request) -> FileController:
    """
    Resolve a scoped FileController from the IoC container stored
    in app.state, ensuring per-request lifecycle and dependency resolution.
    """
    try:
        container = request.app.state.container
        scope = request.state.scope

        controller = await container.resolve("FileController", scope)
        controller.request = request

        return controller

    except Exception as e:
        logger.error(f"[FileRoute] Resolving FileController failed: {e}")
        raise_error(e)


@fileRouter.get("/{category}/{filename}")
async def login(file_controller: FileController = Depends(get_file_controller)):
    return await file_controller.getUploadedFile()
