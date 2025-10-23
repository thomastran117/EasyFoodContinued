from fastapi import APIRouter, Depends, HTTPException

from dtos.reservationDtos import ReservationCreateDto, ReservationUpdateDto
from resources.database_client import SessionLocal
from service.reservationService import (
    create_reservation,
    delete_reservation,
    find_reservation_by_id,
    find_reservations_by_restaurant,
    find_reservations_by_user,
    update_reservation,
)
from service.tokenService import get_current_user, require_auth_token
from utilities.errorRaiser import BadRequestException, raise_error


async def getReservationsByUser(token: str = Depends(require_auth_token)):
    db = SessionLocal()
    try:
        user_payload = get_current_user(token)
        reservations = find_reservations_by_user(db, user_payload["id"])
        return {"message": "user's reservations found", "reservations": reservations}
    except Exception as e:
        raise_error(e)
    finally:
        db.close()


async def getReservationById(id: int):
    db = SessionLocal()
    try:
        if id <= 0:
            raise BadRequestException("Invalid reservation ID")
        reservation = find_reservation_by_id(db, id)
        return {
            "message": f"Reservation with id {id} found",
            "reservation": reservation,
        }
    except Exception as e:
        raise_error(e)
    finally:
        db.close()


async def getReservationsByRestaurant():
    db = SessionLocal()
    try:
        if id <= 0:
            raise BadRequestException("Invalid restaurant ID")
        reservations = find_reservations_by_restaurant(db, id)
        return {
            "message": "restaurant's reservations found",
            "reservations": reservations,
        }
    except Exception as e:
        raise_error(e)
    finally:
        db.close()


async def createReservation(
    id: int, create: ReservationCreateDto, token: str = Depends(require_auth_token)
):
    db = SessionLocal()
    try:
        if id <= 0:
            raise BadRequestException(f"{id} is an invalid restaurant ID")
        user_payload = get_current_user(token)
        reservation = create_reservation(
            db,
            restaurant_id=id,
            user_id=user_payload["id"],
            seats=create.seats,
            occasion=create.occasion,
            details=create.details,
        )
        return {
            "message": f"Reservation {reservation.id} created successfully",
            "reservation_id": reservation.id,
        }
    except Exception as e:
        raise_error(e)
    finally:
        db.close()


async def updateReservation(
    id: int, update: ReservationUpdateDto, token: str = Depends(require_auth_token)
):
    db = SessionLocal()
    try:
        if id <= 0:
            raise BadRequestException(f"{id} is an invalid reservation ID")
        user_payload = get_current_user(token)
        reservation = update_reservation(
            db,
            restaurant_id=id,
            user_id=user_payload["id"],
            seats=update.seats,
            occasion=update.occasion,
            details=update.details,
        )
        return {
            "message": f"Reservation with id {id} updated successfully",
            "reservation_id": id,
        }
    except Exception as e:
        raise_error(e)
    finally:
        db.close()


async def deleteReservation(id: int, token: str = Depends(require_auth_token)):
    db = SessionLocal()
    try:
        if id <= 0:
            raise BadRequestException("Invalid ID")
        user_payload = get_current_user(token)
        delete_reservation(db, id, user_payload["id"])
        return {"message": f"Reservation with id {id} deleted successfully"}
    except Exception as e:
        raise_error(e)
    finally:
        db.close()
