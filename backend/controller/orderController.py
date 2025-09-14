from fastapi import APIRouter, Depends
from service.tokenService import oauth2_scheme, decode_token
from service.orderService import (
    create_order,
    update_order,
    delete_order,
    find_order_by_id,
    find_orders_by_restaurant,
    find_orders_by_user,
)
from dtos.orderDtos import CreateOrderRequest, FoodRequest
from utilities.errorRaiser import raise_error
from utilities.exception import BadRequestException
from resource.alchemy import SessionLocal


def serialize_order(order):
    return {
        "id": order.id,
        "created_at": order.created_at,
        "notes": order.notes,
        "payment_type": order.payment_type,
        "fulfillment_type": order.fulfillment_type,
        "address": order.address,
        "items": [
            {
                "id": of.food.id,
                "name": of.food.name,
                "price": of.food.price,
                "image": of.food.foodUrl,
                "quantity": of.quantity,
            }
            for of in order.order_foods
        ],
    }


async def getOrdersByUser(token: str = Depends(oauth2_scheme)):
    db = SessionLocal()
    try:
        user_payload = decode_token(token)
        orders = find_orders_by_user(db, user_payload["id"])
        orders_response = [serialize_order(order) for order in orders]
        return {"message": "User orders found successfully", "orders": orders_response}
    except Exception as e:
        raise_error(e)
    finally:
        db.close()


async def getOrdersByRestaurant(token: str = Depends(oauth2_scheme)):
    db = SessionLocal()
    try:
        user_payload = decode_token(token)
        orders = find_orders_by_restaurant(db, user_payload["id"])
        orders_response = [serialize_order(order) for order in orders]
        return {
            "message": "Restaurant orders found successfully",
            "orders": orders_response,
        }
    except Exception as e:
        raise_error(e)
    finally:
        db.close()


async def getOrderById(id: int, token: str = Depends(oauth2_scheme)):
    db = SessionLocal()
    try:
        user_payload = decode_token(token)
        if id <= 0:
            raise BadRequestException("Invalid order ID")
        order = find_order_by_id(db, id, user_payload["id"])
        order_response = serialize_order(order)
        return {
            "message": f"Order with id {id} found successfully",
            "order": order_response,
        }
    except Exception as e:
        raise_error(e)
    finally:
        db.close()


async def createOrder(
    data: CreateOrderRequest,
    token: str = Depends(oauth2_scheme),
):
    db = SessionLocal()
    try:
        user_payload = decode_token(token)

        food_requests = [
            {"food_id": item.food_id, "quantity": item.quantity} for item in data.items
        ]

        fulfillment_data = data.fulfillment.dict()
        payment_data = data.payment.dict()
        notes = data.notes

        order = create_order(
            db,
            user_id=user_payload["id"],
            food_requests=food_requests,
            fulfillment=fulfillment_data,
            payment=payment_data,
            notes=notes,
        )

        return {
            "message": f"Order {order.id} created successfully for restaurant {id}",
            "order": order,
        }

    except Exception as e:
        raise_error(e)


async def updateOrder(id: int, token: str = Depends(oauth2_scheme)):
    db = SessionLocal()
    try:
        if id <= 0:
            raise BadRequestException("Invalid order ID")
        user_payload = decode_token(token)
        pass
    except Exception as e:
        raise_error(e)
    finally:
        db.close()


async def deleteOrder(id: int, token: str = Depends(oauth2_scheme)):
    db = SessionLocal()
    try:
        if id <= 0:
            raise BadRequestException("Invalid order ID")
        user_payload = decode_token(token)
        delete_order(db, id, user_payload["id"])
        return {"message": f"Order with ID {id} deleted successfully"}
    except Exception as e:
        print(e)
        raise_error(e)
    finally:
        db.close()
