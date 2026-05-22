import uuid

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from core.database import get_db
from core.security import admin_only
from models.user import User
from schemas.booking import BookingCreate, BookingResponse, BookingUpdate
from services.booking_service import (
    create_booking,
    delete_booking,
    get_all_bookings,
    update_booking,
)

router = APIRouter(prefix="/bookings", tags=["bookings"])


@router.post(
    "",
    response_model=BookingResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_booking_endpoint(
    data: BookingCreate,
    db: Session = Depends(get_db),
):
    return create_booking(db, data)


@router.get("", response_model=list[BookingResponse])
def get_all_bookings_endpoint(
    db: Session = Depends(get_db),
    _: User = Depends(admin_only),
):
    return get_all_bookings(db)


@router.patch("/{id}", response_model=BookingResponse)
def update_booking_endpoint(
    id: uuid.UUID,
    data: BookingUpdate,
    db: Session = Depends(get_db),
    _: User = Depends(admin_only),
):
    return update_booking(db, id, data)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_booking_endpoint(
    id: uuid.UUID,
    db: Session = Depends(get_db),
    _: User = Depends(admin_only),
):
    delete_booking(db, id)
