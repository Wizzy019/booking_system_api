import uuid
from datetime import date, datetime, time
from typing import Annotated, Optional

from pydantic import BaseModel, BeforeValidator, EmailStr

from utils.cleanbasemodel import CleanBaseModel


def _optional_time(v):
    if v is None or v == "":
        return None
    return v


OptionalTime = Annotated[time | None, BeforeValidator(_optional_time)]


class BookingCreate(CleanBaseModel):
    name: str
    email: EmailStr
    date: date
    time_slot: time


class BookingUpdate(CleanBaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    date: Optional[date] = None
    time_slot: OptionalTime = None
    status: Optional[str] = None


class BookingResponse(BaseModel):
    id: uuid.UUID
    name: str
    email: str
    date: date
    time_slot: time
    status: str
    created_at: datetime

    model_config = {"from_attributes": True}
