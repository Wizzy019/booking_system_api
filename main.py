from fastapi import FastAPI

from core.database import create_tables
from routes.auth import router as auth_router
from routes.availability import router as availability_router
from routes.bookings import router as bookings_router

create_tables()

app = FastAPI()

app.include_router(auth_router)
app.include_router(availability_router)
app.include_router(bookings_router)
