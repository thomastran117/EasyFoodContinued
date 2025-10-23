from typing import Optional

from fastapi import APIRouter, Depends, Query

from dtos.restaurantDtos import RestaurantCreateDto, RestaurantUpdateDto
from resources.database_client import SessionLocal
from service.restaurantService import (
    create_restaurant,
    delete_restaurant,
    find_all_restaurants,
    find_restaurant_by_id,
    find_restaurant_by_userid,
    update_restaurant,
)
from service.tokenService import get_current_user, require_auth_token
from utilities.errorRaiser import BadRequestException, raise_error


async def getRestaurant(id: int):
    db = SessionLocal()
    try:
        if id <= 0:
            raise BadRequestException("Invalid ID")
        restaurant = find_restaurant_by_id(db, id)
        return {"message": f"Restaurant with id {id} found", "restaurant": restaurant}
    except Exception as e:
        print(e)
        raise_error(e)
    finally:
        db.close()


async def getRestaurants(
    title: Optional[str] = Query(None),
    description: Optional[str] = Query(None),
    location: Optional[str] = Query(None),
):
    db = SessionLocal()
    try:
        restaurants = find_all_restaurants(
            db, title=title, description=description, location=location
        )
        return {"message": "Restaurants Found", "restaurants": restaurants}
    except Exception as e:
        raise_error(e)
    finally:
        db.close()


async def getUserRestaurant(token: str = Depends(require_auth_token)):
    db = SessionLocal()
    try:
        user_payload = get_current_user(token)
        restaurant = find_restaurant_by_userid(db, user_payload["id"])
        return {"message": "User's restaurant found", "restaurant": restaurant}
    except Exception as e:
        raise_error(e)
    finally:
        db.close()


async def addRestaurant(
    create: RestaurantCreateDto, token: str = Depends(require_auth_token)
):
    db = SessionLocal()
    try:
        user_payload = get_current_user(token)
        restaurant = create_restaurant(
            db,
            owner_id=user_payload["id"],
            name=create.name,
            description=create.description,
            location=create.location,
            logoUrl=create.logoUrl,
        )
        return {
            "message": f"Restaurant {restaurant.id} created successfully",
            "restaurant_id": restaurant.id,
        }
    except Exception as e:
        raise_error(e)
    finally:
        db.close()


async def updateRestaurant(
    update: RestaurantUpdateDto, token: str = Depends(require_auth_token)
):
    db = SessionLocal()
    try:
        user_payload = get_current_user(token)
        restaurant = update_restaurant(
            db,
            owner_id=user_payload["id"],
            name=update.name,
            description=update.description,
            location=update.location,
            logoUrl=update.logoUrl,
        )
        return {
            "message": f"Restaurant with id {restaurant.id} updated successfully",
            "restaurant_id": restaurant.id,
        }
    except Exception as e:
        raise_error(e)
    finally:
        db.close()


async def deleteRestaurant(token: str = Depends(require_auth_token)):
    db = SessionLocal()
    try:
        user_payload = get_current_user(token)
        delete_restaurant(db, user_payload["id"])
        return {"message": f"Restaurant deleted successfully"}
    except Exception as e:
        print(e)
        raise_error(e)
    finally:
        db.close()
