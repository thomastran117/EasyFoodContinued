from fastapi import APIRouter
from controller.fileController import FileController
from resources.container import container

fileController: FileController = container.file_controller

fileRouter = APIRouter()
fileRouter.add_api_route(
    "/{category}/{filename}", fileController.get_file, methods=["GET"]
)
