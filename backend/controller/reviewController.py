from fastapi import APIRouter, HTTPException, Depends
from service.reviewService import (
    create_review,
    update_review,
    delete_review,
    find_review_by_id,
    find_reviews_by_restaurant,
    find_reviews_by_user,
)
from resources.alchemy import SessionLocal
from utilities.errorRaiser import raise_error
from utilities.exception import BadRequestException
from service.tokenService import oauth2_scheme, decode_token
from dtos.reviewDtos import ReviewCreateDto, ReviewUpdateDto


async def getReviewsByUser(token: str = Depends(oauth2_scheme)):
    db = SessionLocal()
    try:
        user_payload = decode_token(token)
        reviews = find_reviews_by_user(db, user_payload["id"])
        return {"message": "user's reviews found", "reviews": reviews}
    except Exception as e:
        raise_error(e)
    finally:
        db.close()


async def getReviewById(id: int):
    db = SessionLocal()
    try:
        if id <= 0:
            raise BadRequestException("Invalid review ID")
        review = find_review_by_id(db, id)
        return {"message": f"Review with id {id} found", "review": review}
    except Exception as e:
        raise_error(e)
    finally:
        db.close()


async def getReviewsByRestaurant(id: int):
    db = SessionLocal()
    try:
        if id <= 0:
            raise BadRequestException("Invalid restaurant ID")
        reviews = find_reviews_by_restaurant(db, id)
        return {"message": f"restaurant with id {id} reviews found", "reviews": reviews}
    except Exception as e:
        raise_error(e)
    finally:
        db.close()


async def createReview(
    id: int, create: ReviewCreateDto, token: str = Depends(oauth2_scheme)
):
    db = SessionLocal()
    try:
        if id <= 0:
            raise BadRequestException(f"{id} is an invalid restaurant ID")
        user_payload = decode_token(token)
        review = create_review(
            db,
            restaurant_id=id,
            user_id=user_payload["id"],
            name=create.name,
            description=create.description,
            rating=create.rating,
        )
        return {
            "message": f"Review {review.id} created successfully",
            "review_id": review.id,
        }
    except Exception as e:
        raise_error(e)
    finally:
        db.close()


async def updateReview(
    id: int, update: ReviewUpdateDto, token: str = Depends(oauth2_scheme)
):
    db = SessionLocal()
    try:
        if id <= 0:
            raise BadRequestException("Invalid reservation ID")
        user_payload = decode_token(token)
        review = update_review(
            db,
            restaurant_id=id,
            user_id=user_payload["id"],
            name=update.name,
            description=update.description,
            rating=update.rating,
        )
        return {
            "message": f"Review with id {id} updated successfully",
            "review_id": review.id,
        }
    except Exception as e:
        raise_error(e)
    finally:
        db.close()


async def deleteReview(id: int, token: str = Depends(oauth2_scheme)):
    db = SessionLocal()
    try:
        if id <= 0:
            raise BadRequestException("Invalid ID")
        user_payload = decode_token(token)
        delete_review(db, id, user_payload["id"])
        return {"message": f"Review with id {id} deleted successfully"}
    except Exception as e:
        raise_error(e)
    finally:
        db.close()
