from resource.alchemy import Review
from utilities.exception import ForbiddenException, NotFoundException
from service.restaurantService import find_restaurant_by_id


def find_review_by_id(db, food_id: int):
    review = db.query(Review).filter(Review.id == food_id).first()
    if not review:
        raise NotFoundException("Review not found.")
    return review


def find_reviews_by_restaurant(db, restaurant_id: int):
    find_restaurant_by_id(db, restaurant_id)
    reviews = db.query(Review).filter(Review.restaurant_id == restaurant_id).all()
    return reviews


def find_reviews_by_user(db, user_id: int):
    reviews = db.query(Review).filter(Review.user_id == user_id).all()
    return reviews


def find_all_reviews(db):
    reviews = db.query(Review).all()
    return reviews


def create_review(
    db, restaurant_id: int, user_id: int, name: str, description: str, rating: float
):
    new_review = Review(
        name=name,
        description=description,
        rating=rating,
        restaurant_id=restaurant_id,
        user_id=user_id,
    )

    db.add(new_review)
    db.commit()
    db.refresh(new_review)
    return new_review


def update_review(
    db,
    review_id: int,
    user_id: int,
    name: str = None,
    description: str = None,
    rating: float = None,
):
    review = user_can_change_review(db, review_id, user_id)

    if name is not None:
        review.name = name
    if description is not None:
        review.description = description
    if rating is not None:
        review.rating = rating

    db.commit()
    db.refresh(review)
    return review


def delete_review(db, review_id, user_id):
    food = user_can_change_review(db, review_id, user_id)

    db.delete(food)
    db.commit()


def user_can_change_review(db, review_id, user_id):
    review = find_review_by_id(db, review_id)
    if review.user_id != user_id:
        raise ForbiddenException("You are not allowed to edit this review")

    return review
