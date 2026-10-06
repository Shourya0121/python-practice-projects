from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session 

from app.dependencies.auth import get_current_admin
from app.schemas.user import UserResponse
from app.database import get_db
from app.models.user import User

router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)

@router.get("/dashboard")
def admin_dashboard(
    current_user: dict = Depends(get_current_admin)
    ):

    return {
        "message": "Welcome to the Admin Dashboard!",
        "users": current_user
    }

@router.get("/users", response_model=list[UserResponse])
def get_all_users(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_admin)
):
    users = db.query(User).all()

    return users