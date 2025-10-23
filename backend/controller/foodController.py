from typing import Optional

from fastapi import APIRouter, Depends, Query

from dtos.foodDtos import FoodCreateDto, FoodUpdateDto
from resources.database_client import SessionLocal
from service.foodService import (
    create_food,
    delete_food,
    find_all_foods,
    find_food_by_id,
    find_foods_by_restaurant,
    find_foods_by_user_restaurant,
    update_food,
)
from service.tokenService import get_current_user, require_auth_token
from utilities.errorRaiser import BadRequestException, raise_error


async def getFood(id: int):
    db = SessionLocal()
    try:
        if id <= 0:
            raise BadRequestException("Invalid ID")
        food = find_food_by_id(db, id)
        return {"message": f"Food with ID {id} found", "food": food}
    except Exception as e:
        raise_error(e)
    finally:
        db.close()


async def getFoods(
    skip: int = Query(0),
    limit: int = Query(5),
    name: Optional[str] = Query(None),
    description: Optional[str] = Query(None),
    priceMin: Optional[float] = Query(None, gt=0),
    priceMax: Optional[float] = Query(None, gt=0),
    tags: Optional[str] = Query(None),
):
    db = SessionLocal()
    try:
        if priceMin is not None and priceMax is not None:
            if priceMax < priceMin:
                raise BadRequestException("Invalid price range")
        result = find_all_foods(
            db,
            skip=skip,
            limit=limit,
            name=name,
            description=description,
            priceMin=priceMin,
            priceMax=priceMax,
            tags=tags,
        )
        return {
            "message": "Foods Found",
            "foods": result["foods"],
            "total": result["total"],
        }
    except Exception as e:
        raise_error(e)
    finally:
        db.close()


async def getFoodsByUserRestaurant(
    skip: int = Query(0),
    limit: int = Query(5),
    token: str = Depends(require_auth_token),
    name: Optional[str] = Query(None),
    description: Optional[str] = Query(None),
    priceMin: Optional[float] = Query(None, gt=0),
    priceMax: Optional[float] = Query(None, gt=0),
    tags: Optional[str] = Query(None),
):
    db = SessionLocal()
    try:
        if priceMin is not None and priceMax is not None:
            if priceMax < priceMin:
                raise BadRequestException("Invalid price range")
        user_payload = get_current_user(token)
        result = find_foods_by_user_restaurant(
            db,
            user_payload["id"],
            skip=skip,
            limit=limit,
            name=name,
            description=description,
            priceMin=priceMin,
            priceMax=priceMax,
            tags=tags,
        )
        return {
            "message": "User's Foods Found",
            "foods": result["foods"],
            "total": result["total"],
        }
    except Exception as e:
        raise_error(e)
    finally:
        db.close()


async def getFoodsByRestaurant(
    id: int,
    skip: int = Query(0),
    limit: int = Query(5),
    name: Optional[str] = Query(None),
    description: Optional[str] = Query(None),
    priceMin: Optional[float] = Query(None, gt=0),
    priceMax: Optional[float] = Query(None, gt=0),
    tags: Optional[str] = Query(None),
):
    db = SessionLocal()
    try:
        if priceMin is not None and priceMax is not None:
            if priceMax < priceMin:
                raise BadRequestException("Invalid price range")
        if id <= 0:
            raise BadRequestException(f"{id} is an Invalid Restaurant ID")
        result = find_foods_by_restaurant(
            db,
            id,
            skip=skip,
            limit=limit,
            name=name,
            description=description,
            priceMin=priceMin,
            priceMax=priceMax,
            tags=tags,
        )
        return {
            "message": "Restaurant's Foods Found",
            "foods": result["foods"],
            "total": result["total"],
        }
    except Exception as e:
        print(e)
        raise_error(e)
    finally:
        db.close()


async def addFood(create: FoodCreateDto, token: str = Depends(require_auth_token)):
    db = SessionLocal()
    try:
        user_payload = get_current_user(token)
        food = create_food(
            db,
            user_id=user_payload["id"],
            name=create.name,
            description=create.description,
            price=create.price,
            foodUrl=create.foodUrl,
            ingredients=create.ingredients,
            calories=create.calories,
            tags=create.tags,
        )
        return {
            "message": f"Food with ID {food.id} created successfully",
            "food_id": food.id,
        }
    except Exception as e:
        print(e)
        raise_error(e)
    finally:
        db.close()


async def updateFood(
    id: int, update: FoodUpdateDto, token: str = Depends(require_auth_token)
):
    db = SessionLocal()
    try:
        if id <= 0:
            raise BadRequestException(f"{id} is an invalid Food ID")
        user_payload = get_current_user(token)
        food = update_food(
            db,
            food_id=id,
            user_id=user_payload["id"],
            name=update.name,
            description=update.description,
            price=update.price,
            foodUrl=update.foodUrl,
            ingredients=update.ingredients,
            calories=update.calories,
            tags=update.tags,
        )
        return {"message": f"Food with ID {id} updated successfully", "food_id": id}
    except Exception as e:
        print(e)
        raise_error(e)
    finally:
        db.close()


async def deleteFood(id: int, token: str = Depends(require_auth_token)):
    db = SessionLocal()
    try:
        if id <= 0:
            raise BadRequestException("Invalid ID")
        user_payload = get_current_user(token)
        delete_food(db, id, user_payload["id"])
        return {"message": f"Food with ID {id} deleted successfully"}
    except Exception as e:
        raise_error(e)
    finally:
        db.close()
