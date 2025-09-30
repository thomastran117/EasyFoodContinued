from resources.alchemy import Order, OrderFood
from sqlalchemy.orm import joinedload
from datetime import datetime
from utilities.errorRaiser import (
    ForbiddenException,
    NotFoundException,
    BadRequestException,
)
from service.restaurantService import find_restaurant_by_id, find_restaurant_by_userid
from service.foodService import get_valid_foods
from service.userService import get_user_by_id


def create_order(
    db,
    user_id: int,
    food_requests: list[dict],
    payment: dict,
    fulfillment: dict,
    notes: str = "",
):
    user = get_user_by_id(db, user_id)
    food_items = get_valid_foods(db, food_requests)

    order = Order(
        user=user,
        payment_name=payment["name"],
        payment_type=payment["type"],
        payment_number=payment["cardNumber"],
        payment_expiry=payment["expiry"],
        payment_cvv=payment["cvv"],
        fulfillment_type=fulfillment["type"],
        address=fulfillment.get("address"),
        notes=notes,
    )

    for item in food_items:
        food = item["food"]
        quantity = item["quantity"]

        order_food = OrderFood(food=food, quantity=quantity)
        order.order_foods.append(order_food)

    db.add(order)
    db.commit()
    db.refresh(order)

    return order


def update_order(
    db,
    order_id: int,
    user_id: int,
    food_requests: list[dict],
    payment: dict,
    fulfillment: dict,
    notes: str = "",
):
    order = find_order_by_id(db, order_id, user_id)

    food_items = get_valid_foods(db, food_requests)
    order.order_foods.clear()

    for item in food_items:
        food = item["food"]
        quantity = item["quantity"]
        order_food = OrderFood(food=food, quantity=quantity)
        order.order_foods.append(order_food)

    if payment:
        if "name" in payment:
            order.payment_name = payment["name"]
        if "type" in payment:
            order.payment_type = payment["type"]
        if "cardNumber" in payment:
            order.payment_number = payment["cardNumber"]
        if "expiry" in payment:
            order.payment_expiry = payment["expiry"]
        if "cvv" in payment:
            order.payment_cvv = payment["cvv"]

    if fulfillment:
        if "type" in fulfillment:
            order.fulfillment_type = fulfillment["type"]
        if "address" in fulfillment:
            order.address = fulfillment["address"]

    if notes is not None:
        order.notes = notes

    db.commit()
    db.refresh(order)

    return order


def delete_order(db, order_id: int, user_id: int):
    order = find_order_by_id(db, order_id, user_id)

    db.delete(order)
    db.commit()


def find_orders_by_user(db, user_id: int):
    orders = (
        db.query(Order)
        .options(joinedload(Order.order_foods).joinedload(OrderFood.food))
        .filter(Order.user_id == user_id)
        .order_by(Order.created_at.desc())
        .all()
    )
    return orders


def find_order_by_id(db, order_id: int, user_id: int):
    order = (
        db.query(Order)
        .options(joinedload(Order.order_foods).joinedload(OrderFood.food))
        .filter(Order.id == order_id)
        .first()
    )

    if not order:
        raise NotFoundException("Order not found")

    if order.user_id != user_id:
        raise ForbiddenException("You are not allowed to view this order")

    return order


def find_orders_by_restaurant(db, user_id: int):
    restaurant = find_restaurant_by_userid(db, user_id)
    orders = (
        db.query(Order)
        .filter(Order.restaurant_id == restaurant.id)
        .order_by(Order.created_at.desc())
        .all()
    )
    return orders
