from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session

from core.database import get_db
from core.security import admin_only, create_access_token, hash_password, verify_password, get_current_user
from models.user import User
from services.avater_service import upload_avater_to_supabase
from schemas.auth import (
    AdminLoginRequest,
    AdminLoginResponse,
    AdminRegisterRequest,
    AdminRegisterResponse,
)

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=AdminLoginResponse)
def admin_login(data: AdminLoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email).first()
    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )
    if user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required",
        )
    return AdminLoginResponse(access_token=create_access_token(user.id))


@router.post(
    "/register_admin",
    response_model=AdminRegisterResponse,
    status_code=status.HTTP_201_CREATED,
)
def register_admin(
    data: AdminRegisterRequest,
    db: Session = Depends(get_db),
    _: User = Depends(admin_only),
):

    if not data.first_name:
        raise HTTPException(400, "first_name is required")

    if not data.last_name:
        raise HTTPException(400, "last_name is required")

    existing = db.query(User).filter(User.email == data.email).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    user = User(
        email=data.email,
        password_hash=hash_password(data.password),
        first_name=data.first_name,
        last_name=data.last_name,
        role="admin",
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@router.get("/me")
def get_user(current_user: User = Depends(get_current_user)):
        return {
        "messagee": "Access granted",
        "user": {
            "id" : current_user.id,
            "email": current_user.email,
            "first_name" : current_user.first_name,
            "last_name": current_user.last_name,
            "role": current_user.role,
            "avater" : current_user.profile_image_path
        }
    }


@router.post("/avatar")
async def upload_avatar(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    file_bytes = await file.read()

    path = await upload_avater_to_supabase(
        file_bytes=file_bytes,
        content_type=file.content_type,
        user_id=str(current_user.id)
    )

    current_user.profile_image_path = path

    db.commit()

    return {
        "message": "Avater Uploaded",
        "path": path
    }