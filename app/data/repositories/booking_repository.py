from sqlalchemy import select
from sqlalchemy.orm import Session

from app.data.models.booking import Booking


def create_booking(
    db: Session,
    farmer_id: int,
    resource_id: int,
    quantity: float,
    total_price: float,
    booking_status: str = "PENDING",
    notes: str | None = None,
) -> Booking:
    booking = Booking(
        farmer_id=farmer_id,
        resource_id=resource_id,
        quantity=quantity,
        total_price=total_price,
        booking_status=booking_status,
        notes=notes,
    )

    db.add(booking)
    db.commit()
    db.refresh(booking)
    return booking


def get_booking_by_id(
    db: Session, booking_id: int
) -> Booking | None:
    return db.get(Booking, booking_id)


def get_bookings_by_farmer(
    db: Session, farmer_id: int
) -> list[Booking]:
    statement = (
        select(Booking)
        .where(Booking.farmer_id == farmer_id)
        .order_by(Booking.booking_date.desc())
    )
    return list(db.scalars(statement).all())


def get_all_bookings(
    db: Session, limit: int = 100
) -> list[Booking]:
    statement = (
        select(Booking)
        .order_by(Booking.booking_date.desc())
        .limit(limit)
    )
    return list(db.scalars(statement).all())


def update_booking_status(
    db: Session,
    booking: Booking,
    booking_status: str,
) -> Booking:
    booking.booking_status = booking_status
    db.commit()
    db.refresh(booking)
    return booking


def delete_booking(
    db: Session, booking: Booking
) -> None:
    db.delete(booking)
    db.commit()
