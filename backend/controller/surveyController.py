from typing import Optional
from fastapi import APIRouter, Query, Depends
from utilities.errorRaiser import raise_error, BadRequestException, NotImplementedException
from resources.alchemy import SessionLocal
from service.tokenService import oauth2_scheme, get_current_user
from service.surveyService import (
    create_survey,
    update_survey,
    delete_survey,
    find_survey_by_id,
    find_surveys_by_user,
    find_all_surveys,
)
from dtos.surveyDtos import SurveyCreateDto, SurveyUpdateDto


async def getSurvey(id: int, token: str = Depends(oauth2_scheme)):
    db = SessionLocal()
    try:
        if id <= 0:
            raise BadRequestException(f"{id} is an invalid reservation ID")
        user_payload = get_current_user(token)
        survey = find_survey_by_id(db, id, user_payload["id"])
        return {"message": "survey found", "survey": survey}
    except Exception as e:
        raise_error(e)
    finally:
        db.close()


async def getSurveysByUser(token: str = Depends(oauth2_scheme)):
    db = SessionLocal()
    try:
        user_payload = get_current_user(token)
        surveys = find_surveys_by_user(db, user_payload["id"])
        return {"message": "surveys found", "surveys": surveys}
    except Exception as e:
        raise_error(e)
    finally:
        db.close()


async def getSurveys():
    db = SessionLocal()
    try:
        raise NotImplementedError("This route is not implemented yet")
    except Exception as e:
        raise_error(e)
    finally:
        db.close()


async def createSurvey(create: SurveyCreateDto, token: str = Depends(oauth2_scheme)):
    db = SessionLocal()
    try:
        user_payload = get_current_user(token)
        survey = create_survey(
            db,
            user_id=user_payload["id"],
            one=create.browsing,
            two=create.ordering,
            three=create.design,
            four=create.suggestions,
            rating=create.rating,
        )
        return {"message": "survey created", "survey_id": survey.id}
    except Exception as e:
        raise_error(e)
    finally:
        db.close()


async def updateSurvey(
    id: int, update: SurveyUpdateDto, token: str = Depends(oauth2_scheme)
):
    db = SessionLocal()
    try:
        if id <= 0:
            raise BadRequestException(f"{id} is an invalid reservation ID")
        user_payload = get_current_user(token)
        survey = update_survey(
            db,
            survey_id=id,
            user_id=user_payload[id],
            one=update.browsing,
            two=update.ordering,
            three=update.design,
            four=update.suggestions,
            rating=update.rating,
        )
        return {"message": "survey updated", "survey_id": survey.id}
    except Exception as e:
        raise_error(e)
    finally:
        db.close()


async def deleteSurvey(id: int, token: str = Depends(oauth2_scheme)):
    db = SessionLocal()
    try:
        if id <= 0:
            raise BadRequestException(f"{id} is an invalid reservation ID")
        user_payload = decode_token(token)
        survey = delete_survey(db, id, user_payload["id"])
        return {"message": "survey deleted", "survey_id": survey.id}
    except Exception as e:
        raise_error(e)
    finally:
        db.close()
