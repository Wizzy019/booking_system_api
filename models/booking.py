import uuid
from datetime import date, datetime, time

from sqlalchemy import Date, DateTime, Text, Time, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from core.database import Base


class Booking(Base):
    __tablename__ = "bk_sys_bookings"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()")
    )
    name: Mapped[str] = mapped_column(Text, nullable=False)
    email: Mapped[str] = mapped_column(Text, nullable=False)
    date: Mapped[date] = mapped_column(Date, nullable=False)
    time_slot: Mapped[time] = mapped_column(Time, nullable=False)
    status: Mapped[str] = mapped_column(Text, server_default=text("'booked'"))
    created_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=text("NOW()")
    )
