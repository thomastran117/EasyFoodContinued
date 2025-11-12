from fastapi import APIRouter, Depends, Request
from controller.fileController import FileController

fileRouter = APIRouter(tags=["File"])


async def get_file_controller(request: Request) -> FileController:
    """
    Resolve a scoped FileController from the IoC container stored
    in app.state, ensuring per-request lifecycle and dependency resolution.
    """
    container = request.app.state.container

    async with container.create_scope() as scope:
        controller = await container.resolve("FileController", scope)
        controller.request = request
        return controller


@fileRouter.get("/{category}/{filename}")
async def login(file_controller: FileController = Depends(get_file_controller)):
    return await file_controller.get_file()
