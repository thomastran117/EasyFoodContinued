from resources.alchemy import Food
from utilities.errorRaiser import (
    ForbiddenException,
    NotFoundException,
    BadRequestException,
)
from service.restaurantService import find_restaurant_by_id, find_restaurant_by_userid
from utilities.imageValidator import is_valid_image_url


def find_food_by_id(db, food_id: int):

    food = db.query(Food).filter(Food.id == food_id).first()
    if not food:
        raise NotFoundException("Food not found.")
    return food


def find_all_foods(
    db,
    skip: int = 0,
    limit: int = 5,
    name=None,
    description=None,
    priceMin=None,
    priceMax=None,
    tags=None,
):
    query = db.query(Food)

    if name:
        query = query.filter(Food.name.ilike(f"%{name}%"))
    if description:
        query = query.filter(Food.description.ilike(f"%{description}%"))
    if priceMin is not None:
        query = query.filter(Food.price >= priceMin)
    if priceMax is not None:
        query = query.filter(Food.price <= priceMax)
    if tags:
        query = query.filter(Food.tags.ilike(f"%{tags}%"))

    total = query.count()
    foods = query.offset(skip).limit(limit).all()

    return {"total": total, "foods": foods}


def find_foods_by_user_restaurant(
    db,
    user_id: int,
    skip: int = 0,
    limit: int = 5,
    name=None,
    description=None,
    priceMin=None,
    priceMax=None,
    tags=None,
):
    restaurant = find_restaurant_by_userid(db, user_id)
    query = db.query(Food).filter(Food.restaurant_id == restaurant.id)

    if name:
        query = query.filter(Food.name.ilike(f"%{name}%"))
    if description:
        query = query.filter(Food.description.ilike(f"%{description}%"))
    if priceMin is not None:
        query = query.filter(Food.price >= priceMin)
    if priceMax is not None:
        query = query.filter(Food.price <= priceMax)
    if tags:
        query = query.filter(Food.tags.ilike(f"%{tags}%"))

    total = query.count()
    foods = query.order_by(Food.id).offset(skip).limit(limit).all()

    return {"total": total, "foods": foods}


def find_foods_by_restaurant(
    db,
    restaurant_id: int,
    skip: int = 0,
    limit: int = 5,
    name=None,
    description=None,
    priceMin=None,
    priceMax=None,
    tags=None,
):
    find_restaurant_by_id(db, restaurant_id)

    query = db.query(Food).filter(Food.restaurant_id == restaurant_id)

    if name:
        query = query.filter(Food.name.ilike(f"%{name}%"))
    if description:
        query = query.filter(Food.description.ilike(f"%{description}%"))
    if priceMin is not None:
        query = query.filter(Food.price >= priceMin)
    if priceMax is not None:
        query = query.filter(Food.price <= priceMax)
    if tags:
        query = query.filter(Food.tags.ilike(f"%{tags}%"))

    total = query.count()
    foods = query.order_by(Food.id).offset(skip).limit(limit).all()

    return {"total": total, "foods": foods}


def create_food(
    db,
    user_id: int,
    name: str,
    description: str,
    price: float,
    foodUrl: str,
    calories: int = None,
    tags: str = None,
    ingredients: str = None,
):
    if not is_valid_image_url(foodUrl):
        raise BadRequestException("Invalid image URL")

    restaurant = find_restaurant_by_userid(db, user_id)

    new_food = Food(
        name=name,
        description=description,
        price=price,
        foodUrl=foodUrl,
        restaurant_id=restaurant.id,
    )

    if calories is not None:
        new_food.calories = calories
    if tags is not None:
        new_food.tags = tags
    if ingredients is not None:
        new_food.ingredients = ingredients

    db.add(new_food)
    db.commit()
    db.refresh(new_food)
    return new_food


def update_food(
    db,
    food_id: int,
    user_id: int,
    name: str = None,
    description: str = None,
    price: float = None,
    foodUrl: str = None,
    calories: int = None,
    tags: str = None,
    ingredients: str = None,
):
    if not is_valid_image_url(foodUrl):
        raise BadRequestException("Invalid image URL")

    restaurant = find_restaurant_by_userid(db, owner_id=user_id)
    food = find_food_by_id(db, food_id)

    if food.restaurant_id != restaurant.id:
        raise ForbiddenException("You are not allowed to edit this food")

    if name is not None:
        food.name = name
    if description is not None:
        food.description = description
    if price is not None:
        food.price = price
    if foodUrl is not None:
        food.foodUrl = foodUrl
    if calories is not None:
        food.calories = calories
    if tags is not None:
        food.tags = tags
    if ingredients is not None:
        food.ingredients = ingredients

    db.commit()
    db.refresh(food)
    return food


def delete_food(db, food_id, user_id):
    restaurant = find_restaurant_by_userid(db, owner_id=user_id)
    food = find_food_by_id(db, food_id)

    if food.restaurant_id != restaurant.id:
        raise ForbiddenException("You are not allowed to delete this food")

    db.delete(food)
    db.commit()


def get_food_from_order(db):
    pass


def get_food_by_lists(db, food_ids: list[int]):
    foods = db.query(Food).filter(Food.id.in_(food_ids)).all()

    if not foods:
        raise BadRequestException("No valid food items were found")

    return foods


def get_valid_foods(db, food_requests: list[dict]):
    food_ids = [item["food_id"] for item in food_requests]

    foods = db.query(Food).filter(Food.id.in_(food_ids)).all()

    if not foods:
        raise BadRequestException("No valid food items were found")

    food_map = {food.id: food for food in foods}

    result = []

    for item in food_requests:
        food_id = item.get("food_id")
        quantity = item.get("quantity", 1)

        food = food_map.get(food_id)
        if not food:
            continue

        result.append({"food": food, "quantity": quantity})

    if not result:
        raise BadRequestException("No valid food items matched the restaurant")

    return result
