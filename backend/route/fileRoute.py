from fastapi import APIRouter
from controller.fileController import FileController
from resources.container import class_container

fileController: FileController = class_container.get_file_controller()

fileRouter = APIRouter()
fileRouter.add_api_route(
    "/{category}/{filename}", fileController.get_file, methods=["GET"]
)
