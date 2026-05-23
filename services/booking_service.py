import uuid
from datetime import date, time

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from models.availability import Availability
from models.booking import Booking
from schemas.booking import BookingCreate, BookingUpdate


def _date_to_day_of_week(booking_date: date) -> int:
    # Sunday=0, Monday=1, ... Saturday=6
    return (booking_date.weekday() + 1) % 7


def _is_slot_available(
    db: Session, booking_date: date, time_slot: time
) -> bool:
    day_of_week = _date_to_day_of_week(booking_date)
    records = (
        db.query(Availability)
        .filter(Availability.day_of_week == day_of_week)
        .all()
    )
    for record in records:
        if record.start_time <= time_slot < record.end_time:
            return True
    return False


def _booking_exists(db: Session, booking_date: date, time_slot: time) -> bool:
    return (
        db.query(Booking)
        .filter(Booking.date == booking_date, Booking.time_slot == time_slot)
        .first()
        is not None
    )


def create_booking(db: Session, data: BookingCreate) -> Booking:
    if not _is_slot_available(db, data.date, data.time_slot):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Slot unavailable",
        )

    if _booking_exists(db, data.date, data.time_slot):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Already booked",
        )

    booking = Booking(
        name=data.name,
        email=data.email,
        date=data.date,
        time_slot=data.time_slot,
        status="pending",
    )
    db.add(booking)
    db.commit()
    db.refresh(booking)
    return booking


def get_all_bookings(db: Session) -> list[Booking]:
    return (
        db.query(Booking)
        .order_by(Booking.date, Booking.time_slot)
        .all()
    )


def update_booking(db: Session, id: uuid.UUID, data: BookingUpdate) -> Booking:
    booking = db.get(Booking, id)
    if not booking:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Booking not found",
        )

    if "name" in data.model_fields_set and data.name is not None:
        booking.name = data.name
    if "email" in data.model_fields_set and data.email is not None:
        booking.email = data.email
    if "date" in data.model_fields_set and data.date is not None:
        booking.date = data.date
    if "time_slot" in data.model_fields_set and data.time_slot is not None:
        booking.time_slot = data.time_slot
    if "status" in data.model_fields_set and data.status is not None:
        booking.status = data.status

    conflict = (
        db.query(Booking)
        .filter(
            Booking.id != id,
            Booking.date == booking.date,
            Booking.time_slot == booking.time_slot,
        )
        .first()
    )
    if conflict:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Slot already booked",
        )

    db.commit()
    db.refresh(booking)
    return booking


def delete_booking(db: Session, id: uuid.UUID) -> None:
    booking = db.get(Booking, id)
    if not booking:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Booking not found",
        )

    db.delete(booking)
    db.commit()
