from sqlalchemy import select
from sqlalchemy.orm import Session

from app.data.models.booking import Booking
from app.data.models.resource import Resource
from app.data.repositories.booking_repository import (
    create_booking,
    get_booking_by_id,
    get_bookings_by_farmer,
    get_all_bookings,
    update_booking_status,
    delete_booking,
)


class BookingError(Exception):
    pass


def create_farmer_booking(
    db: Session,
    farmer_id: int,
    resource_id: int,
    quantity: float,
    notes: str | None = None,
) -> Booking:
    if quantity <= 0:
        raise BookingError("Quantity must be greater than zero.")

    try:
        # Lock the resource row while checking and reducing stock.
        resource = db.execute(
            select(Resource)
            .where(Resource.id == resource_id)
            .with_for_update()
        ).scalar_one_or_none()

        if resource is None:
            raise BookingError("Resource not found.")

        if not resource.is_available:
            raise BookingError("Resource is currently unavailable.")

        if resource.available_quantity < quantity:
            raise BookingError("Insufficient resource stock.")

        total_price = round(resource.price_per_unit * quantity, 2)

        resource.available_quantity -= quantity
        if resource.available_quantity == 0:
            resource.is_available = False

        booking = Booking(
            farmer_id=farmer_id,
            resource_id=resource_id,
            quantity=quantity,
            total_price=total_price,
            booking_status="CONFIRMED",
            notes=notes,
        )

        db.add(booking)
        db.commit()
        db.refresh(booking)
        return booking

    except Exception:
        db.rollback()
        raise


def find_booking(db: Session, booking_id: int):
    return get_booking_by_id(db, booking_id)


def find_bookings_by_farmer(db: Session, farmer_id: int):
    return get_bookings_by_farmer(db, farmer_id)


def find_all_bookings(db: Session, limit: int = 100):
    return get_all_bookings(db, limit)


def change_booking_status(
    db: Session,
    booking_id: int,
    new_status: str,
):
    allowed_statuses = {
        "PENDING", "CONFIRMED", "CANCELLED", "COMPLETED"
    }

    if new_status not in allowed_statuses:
        raise BookingError("Invalid booking status.")

    booking = get_booking_by_id(db, booking_id)
    if booking is None:
        raise BookingError("Booking not found.")

    if booking.booking_status == "CANCELLED":
        raise BookingError("Cancelled bookings cannot be changed.")

    if booking.booking_status == "COMPLETED":
        raise BookingError("Completed bookings cannot be changed.")

    if new_status == "CANCELLED" and booking.booking_status == "CONFIRMED":
        resource = db.execute(
            select(Resource)
            .where(Resource.id == booking.resource_id)
            .with_for_update()
        ).scalar_one_or_none()

        if resource is not None:
            resource.available_quantity += booking.quantity
            resource.is_available = True

    return update_booking_status(db, booking, new_status)


def remove_booking(db: Session, booking_id: int):
    booking = get_booking_by_id(db, booking_id)
    if booking is None:
        raise BookingError("Booking not found.")

    if booking.booking_status == "CONFIRMED":
        raise BookingError(
            "Cancel the booking first to restore resource stock."
        )

    delete_booking(db, booking)
