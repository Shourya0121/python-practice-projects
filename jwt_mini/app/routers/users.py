from fastapi import APIRouter, Depends


from app.dependencies.auth import get_current_user

router = APIRouter(
    prefix= "/users",
    tags=["users"]
)

@router.get("/me")
def get_me(current_user: dict = Depends(get_current_user)):

    return {
        "message": "You are authenticated",
        "token": current_user
    }