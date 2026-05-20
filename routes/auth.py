from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from core.database import get_db
from core.security import hash_password
from models.user import User
from schemas.auth import AdminRegisterRequest, AdminRegisterResponse

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(
    "/register_admin",
    response_model=AdminRegisterResponse,
    status_code=status.HTTP_201_CREATED,
)
def register_admin(
    data: AdminRegisterRequest,
    db: Session = Depends(get_db),
):
    existing = db.query(User).filter(User.email == data.email).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    user = User(
        email=data.email,
        password_hash=hash_password(data.password),
        role="admin",
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
