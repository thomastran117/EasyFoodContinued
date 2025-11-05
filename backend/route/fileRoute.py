from fastapi import APIRouter, Depends
from controller.fileController import FileController
from resources.container import container

fileRouter = APIRouter(tags=["File"])


def get_file_controller() -> FileController:
    """Resolves an FileController with lifetimes managed by the container."""
    with container.create_scope() as scope:
        return container.resolve("FileController", scope)


@fileRouter.get("/{category}/{filename}")
async def login(file_controller: FileController = Depends(get_file_controller)):
    return await file_controller.get_file()
