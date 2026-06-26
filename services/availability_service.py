import uuid
from datetime import date, datetime, timedelta, time

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from models.availability import Availability
from models.booking import Booking
from schemas.availability import AvailabilityCreate, AvailabilityUpdate, SlotsResponse


def _has_time_conflict(
    day_of_week: int,
    start_time: time,
    end_time: time,
    existing: Availability,
) -> bool:
    return (
        existing.day_of_week == day_of_week
        and start_time < existing.end_time
        and end_time > existing.start_time
    )


def create_availability(db: Session, data: AvailabilityCreate) -> Availability:
    if data.start_time >= data.end_time:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="start_time must be before end_time",
        )

    records = db.query(Availability).all()
    for record in records:
        if _has_time_conflict(
            data.day_of_week, data.start_time, data.end_time, record
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Time conflict",
            )

    availability = Availability(
        day_of_week=data.day_of_week,
        start_time=data.start_time,
        end_time=data.end_time,
    )
    db.add(availability)
    db.commit()
    db.refresh(availability)
    return availability


def get_all_availability(db: Session) -> list[Availability]:
    return (
        db.query(Availability)
        .order_by(Availability.day_of_week, Availability.start_time)
        .all()
    )

def _date_to_day_of_week(booking_date: date) -> int:
    return booking_date.weekday()

SLOT_DURATION = 90


def generate_slots(
    start_time: time,
    end_time: time,
) -> list[time]:
    slots = []

    current = datetime.combine(
        datetime.today(),
        start_time,
    )

    end = datetime.combine(
        datetime.today(),
        end_time,
    )

    while current + timedelta(
        minutes=SLOT_DURATION
    ) <= end:
        slots.append(current.time())
        current += timedelta(
            minutes=SLOT_DURATION
        )

    return slots


# def get_available_slots(db: Session, booking_date: date,) -> SlotResponse:
#     day_of_week = _date_to_day_of_week(
#         booking_date
#     )

#     selected_date = booking_date

#     availability = (
#         db.query(Availability)
#         .filter(
#             Availability.day_of_week
#             == day_of_week
#         )
#         .first()
#     )

#     if not availability:
#         return SlotsResponse(
#         available=[],
#         booked=[]
#     )


#     generated_slots = generate_slots(
#         availability.start_time,
#         availability.end_time,
#     )

#     bookings = (
#         db.query(Booking)
#         .filter(Booking.date == selected_date)
#         .all()
#     )

#     booked_times = {
#         booking.time_slot
#         for booking in bookings
#     }

#     available_slots = [
#         slot
#         for slot in generated_slots
#         if slot not in booked_times
#     ]

#     return SlotsResponse(
#         available=available_slots,
#         booked=list(booked_times)
#     )

def get_slots(db: Session, booking_date: date) -> SlotsResponse:
    day_of_week = _date_to_day_of_week(booking_date)

    availability = (
        db.query(Availability)
        .filter(Availability.day_of_week == day_of_week)
        .first()
    )

    if not availability:
        return SlotsResponse(available=[], booked=[])

    generated_slots = generate_slots(
        availability.start_time,
        availability.end_time,
    )

    bookings = (
        db.query(Booking)
        .filter(Booking.date == booking_date)
        .all()
    )

    booked_times = {
        booking.time_slot
        for booking in bookings
    }

    available_slots = [
        slot for slot in generated_slots
        if slot not in booked_times
    ]

    return SlotsResponse(
        available=available_slots,
        booked=list(booked_times),
    )


def update_availability(
    db: Session, id: uuid.UUID, data: AvailabilityUpdate
) -> Availability:
    record = db.get(Availability, id)
    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not found",
        )

    day_of_week = record.day_of_week
    start_time = record.start_time
    end_time = record.end_time

    if "day_of_week" in data.model_fields_set and data.day_of_week is not None:
        day_of_week = data.day_of_week
    if "start_time" in data.model_fields_set and data.start_time is not None:
        start_time = data.start_time
    if "end_time" in data.model_fields_set and data.end_time is not None:
        end_time = data.end_time

    if start_time >= end_time:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="start_time must be before end_time",
        )

    others = db.query(Availability).filter(Availability.id != id).all()
    for existing in others:
        if _has_time_conflict(day_of_week, start_time, end_time, existing):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Time conflict",
            )

    record.day_of_week = day_of_week
    record.start_time = start_time
    record.end_time = end_time

    db.commit()
    db.refresh(record)
    return record


def delete_availability(db: Session, id: uuid.UUID) -> None:
    record = db.get(Availability, id)
    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not found",
        )

    db.delete(record)
    db.commit()
