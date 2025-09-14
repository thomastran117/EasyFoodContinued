from fastapi import APIRouter
from controller.comboController import (
    getCombo,
    getCombos,
    createCombo,
    updateCombo,
    deleteCombo,
)

comboRouter = APIRouter()
comboRouter.add_api_route("/", getCombos, methods=["GET"])
comboRouter.add_api_route("/{id}", getCombo, methods=["GET"])
comboRouter.add_api_route("/", createCombo, methods=["POST"])
comboRouter.add_api_route("/{id}", updateCombo, methods=["PUT"])
comboRouter.add_api_route("/{id}", deleteCombo, methods=["DELETE"])
