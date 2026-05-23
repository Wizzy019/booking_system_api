import uuid

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from core.database import get_db
from core.security import admin_only
from schemas.availability import (
    AvailabilityCreate,
    AvailabilityResponse,
    AvailabilityUpdate,
)
from services.availability_service import (
    create_availability,
    delete_availability,
    get_all_availability,
    update_availability,
)

router = APIRouter(prefix="/availability", tags=["availability"])


@router.post(
    "",
    response_model=AvailabilityResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(admin_only)]
)
def create_availability_endpoint(
    data: AvailabilityCreate,
    db: Session = Depends(get_db),
):
    return create_availability(db, data)


@router.get("", response_model=list[AvailabilityResponse])
def get_all_availability_endpoint(db: Session = Depends(get_db)):
    return get_all_availability(db)
    

@router.patch("/{id}", response_model=AvailabilityResponse, dependencies=[Depends(admin_only)])
def update_availability_endpoint(
    id: uuid.UUID,
    data: AvailabilityUpdate,
    db: Session = Depends(get_db),
):
    return update_availability(db, id, data)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(admin_only)])
def delete_availability_endpoint(
    id: uuid.UUID,
    db: Session = Depends(get_db),
):
    delete_availability(db, id)
