from fastapi import APIRouter

from controller.surveyController import (
    createSurvey,
    deleteSurvey,
    getSurvey,
    getSurveys,
    getSurveysByUser,
    updateSurvey,
)

surveyRouter = APIRouter()
surveyRouter.add_api_route("/", getSurveys, methods=["GET"])
surveyRouter.add_api_route("/user", getSurveysByUser, methods=["GET"])
surveyRouter.add_api_route("/{id}", getSurvey, methods=["GET"])
surveyRouter.add_api_route("/", createSurvey, methods=["POST"])
surveyRouter.add_api_route("/{id}", updateSurvey, methods=["PUT"])
surveyRouter.add_api_route("/{id}", deleteSurvey, methods=["DELETE"])
