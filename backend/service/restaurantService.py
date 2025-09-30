from resources.alchemy import Restaurant
from utilities.errorRaiser import (
    ConflictException,
    ForbiddenException,
    NotFoundException,
    BadRequestException,
)
from utilities.imageValidator import is_valid_image_url


def find_restaurant_by_id(db, restaurant_id: int):
    restaurant = db.query(Restaurant).filter(Restaurant.id == restaurant_id).first()
    if not restaurant:
        raise NotFoundException("Restaurant not found.")
    return restaurant


def find_restaurant_by_userid(db, owner_id: int):
    restaurant = db.query(Restaurant).filter(Restaurant.owner_id == owner_id).first()
    if not restaurant:
        raise NotFoundException("User's restaurant not found.")
    return restaurant


def find_all_restaurants(
    db, title: str = None, description: str = None, location: str = None
):
    query = db.query(Restaurant)

    if title:
        query = query.filter(Restaurant.name.ilike(f"%{title}%"))
    if description:
        query = query.filter(Restaurant.description.ilike(f"%{description}%"))
    if location:
        query = query.filter(Restaurant.location.ilike(f"%{location}%"))

    restaurants = query.all()
    return restaurants


def create_restaurant(
    db, owner_id: int, name: str, description: str, location: str, logoUrl: str
):
    if not is_valid_image_url(logoUrl):
        raise BadRequestException("Invalid image URL")

    existing_restaurant = (
        db.query(Restaurant).filter(Restaurant.owner_id == owner_id).first()
    )
    if existing_restaurant:
        raise ConflictException("User owns a restaurant already.")

    new_restaurant = Restaurant(
        name=name,
        description=description,
        location=location,
        logoUrl=logoUrl,
        owner_id=owner_id,
    )

    db.add(new_restaurant)
    db.commit()
    db.refresh(new_restaurant)
    return new_restaurant


def update_restaurant(
    db,
    owner_id: int,
    name: str = None,
    description: str = None,
    location: str = None,
    logoUrl: str = None,
):
    if not is_valid_image_url(logoUrl):
        raise BadRequestException("Invalid image URL")

    restaurant = find_restaurant_by_userid(db, owner_id)

    if name is not None:
        restaurant.name = name
    if description is not None:
        restaurant.description = description
    if location is not None:
        restaurant.location = location
    if logoUrl is not None:
        restaurant.logoUrl = logoUrl

    db.commit()
    db.refresh(restaurant)
    return restaurant


def delete_restaurant(db, owner_id: int):
    restaurant = find_restaurant_by_userid(db, owner_id)

    db.delete(restaurant)
    db.commit()


def user_can_change_restaurant(db, restaurant_id, owner_id):
    restaurant = find_restaurant_by_id(db, restaurant_id)

    if restaurant.owner_id != owner_id:
        raise ForbiddenException("You are not allowed to edit this restaurant")

    return restaurant
