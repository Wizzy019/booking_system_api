import uuid

from pydantic import BaseModel, EmailStr

from utils.cleanbasemodel import CleanBaseModel


class AdminRegisterRequest(CleanBaseModel):
    email: EmailStr
    password: str
    first_name: str
    last_name: str
    

class AdminRegisterResponse(BaseModel):
    id: uuid.UUID
    email: str
    first_name: str
    last_name: str
    role: str

    model_config = {"from_attributes": True}


class AdminLoginRequest(CleanBaseModel):
    email: EmailStr
    password: str


class AdminLoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
