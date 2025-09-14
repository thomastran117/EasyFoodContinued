from resource.alchemy import Reservation
from utilities.exception import ForbiddenException, NotFoundException
from service.restaurantService import find_restaurant_by_id


def find_reservation_by_id(db, food_id: int):
    review = db.query(Reservation).filter(Reservation.id == food_id).first()
    if not review:
        raise NotFoundException("Reservation not found.")
    return review


def find_reservations_by_restaurant(db, restaurant_id: int):
    find_restaurant_by_id(db, restaurant_id)
    reviews = (
        db.query(Reservation).filter(Reservation.restaurant_id == restaurant_id).all()
    )
    return reviews


def find_reservations_by_user(db, user_id: int):
    reviews = db.query(Reservation).filter(Reservation.user_id == user_id).all()
    return reviews


def find_all_reservations(db):
    reviews = db.query(Reservation).all()
    return reviews


def create_reservation(
    db, restaurant_id: int, user_id: int, seat: int, occasion: str, details: str
):
    new_review = Reservation(
        seat=seat,
        occasion=occasion,
        details=details,
        restaurant_id=restaurant_id,
        user_id=user_id,
    )

    db.add(new_review)
    db.commit()
    db.refresh(new_review)
    return new_review


def update_reservation(
    db,
    review_id: int,
    user_id: int,
    seat: int = None,
    occasion: str = None,
    details: str = None,
):
    review = user_can_change_reservation(db, review_id, user_id)

    if seat is not None:
        review.seat = seat
    if occasion is not None:
        review.occasion = occasion
    if details is not None:
        review.details = details

    db.commit()
    db.refresh(review)
    return review


def delete_reservation(db, review_id, user_id):
    food = user_can_change_reservation(db, review_id, user_id)

    db.delete(food)
    db.commit()


def user_can_change_reservation(db, review_id, user_id):
    review = find_reservation_by_id(db, review_id)
    if review.user_id != user_id:
        raise ForbiddenException("You are not allowed to edit this reservation")

    return review
