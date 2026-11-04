from fastapi import APIRouter, Depends, HTTPException, status
from typing import Annotated
from fastapi import Form
from sqlalchemy import select
from sqlalchemy.orm import session
from sqlalchemy.exc import IntegrityError

from app.db.session import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse
from app.services.auth import hash_password, verify_password
from app.services.token import create_access_token
from app.schemas.user import UserResponse
from app.core.security import get_current_user


router = APIRouter(prefix="/auth", tags=["Authentication"])

# FOR REGISTER THE USER
@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def register_user(
    user_data: UserCreate,
    db: session = Depends(get_db),
):
    existing_user = db.scalar(
        select(User).where(
            (User.username == user_data.username)
            | (User.email == user_data.email)
        )
    )

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username or email is already registered",
        )

    user = User(
        username=user_data.username,
        email=user_data.email,
        hashed_password=hash_password(user_data.password),
    )

    try:
        db.add(user)
        db.commit()
        db.refresh(user)

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username and email already registered",
        )

    return user
# FOR USER LOGIN ROUTER
@router.post("/login")
def login_user(
    username: Annotated[str, Form()],
    password: Annotated[str, Form()],
    db: session = Depends(get_db),
):
    user = db.scalar(
        select(User).where(User.username == username)
    )

    if not user or not verify_password(
        password,
        user.hashed_password,
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authentication": "Bearer"},
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive User",
        )

    access_token = create_access_token(subject=str(user.id))

    return {
        "access_token": access_token,
        "token_type": "Bearer",
    }

# RESPONSE MODEL FOR USER
@router.get("/me", response_model=UserResponse)
def get_my_profile(
        current_user: User = Depends(get_current_user),
):
    return current_user