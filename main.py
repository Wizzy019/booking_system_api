from fastapi import FastAPI

from core.database import create_tables
from routes.auth import router as auth_router

create_tables()

app = FastAPI()

app.include_router(auth_router)
