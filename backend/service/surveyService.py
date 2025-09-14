from resource.alchemy import Survey
from utilities.exception import ForbiddenException, NotFoundException


def find_survey_by_id(db, survey_id: int, user_id: int):
    survey = db.query(Survey).filter(Survey.id == survey_id).first()
    if not survey:
        raise NotFoundException("Survey not found.")

    if survey.user_id != user_id:
        raise ForbiddenException("You are not allowed to edit this survey response")

    return survey


def find_surveys_by_user(db, user_id: int):
    surveys = db.query(Survey).filter(Survey.user_id == user_id).all()
    return surveys


def find_all_surveys(db):
    surveys = db.query(Survey).all()
    return surveys


def create_survey(
    db, user_id: int, one: str, two: str, three: str, four: str, rating: float
):
    new_survey = Survey(
        question_one=one,
        question_two=two,
        question_three=three,
        question_four=four,
        rating=rating,
        user_id=user_id,
    )

    db.add(new_survey)
    db.commit()
    db.refresh(new_survey)
    return new_survey


def update_survey(
    db,
    survey_id: int,
    user_id: int,
    one: str = None,
    two: str = None,
    three: str = None,
    four: str = None,
    rating: float = None,
):
    survey = find_survey_by_id(db, survey_id, user_id)

    if one is not None:
        survey.question_one = one
    if two is not None:
        survey.question_two = two
    if three is not None:
        survey.question_three = three
    if four is not None:
        survey.question_four = four
    if rating is not None:
        survey.rating = rating

    db.commit()
    db.refresh(survey)
    return survey


def delete_survey(db, survey_id, user_id):
    survey = find_survey_by_id(db, survey_id, user_id)

    db.delete(survey)
    db.commit()

    return survey
