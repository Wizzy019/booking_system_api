import uuid
from datetime import time
from typing import Annotated, Optional

from pydantic import BaseModel, BeforeValidator

from utils.cleanbasemodel import CleanBaseModel


def _optional_time(v):
    if v is None or v == "":
        return None
    return v


OptionalTime = Annotated[time | None, BeforeValidator(_optional_time)]


class AvailabilityCreate(CleanBaseModel):
    day_of_week: int
    start_time: time
    end_time: time


class AvailabilityUpdate(CleanBaseModel):
    day_of_week: Optional[int] = None
    start_time: OptionalTime = None
    end_time: OptionalTime = None


class AvailabilityResponse(BaseModel):
    id: uuid.UUID
    day_of_week: int
    start_time: time
    end_time: time

    model_config = {"from_attributes": True}

class SlotsResponse(BaseModel):
    available: list[time]
    booked: list[time]