import uuid

from pydantic import BaseModel, EmailStr


class AdminRegisterRequest(BaseModel):
    email: EmailStr
    password: str


class AdminRegisterResponse(BaseModel):
    id: uuid.UUID
    email: str
    role: str

    model_config = {"from_attributes": True}
