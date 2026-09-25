from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import session

from app.database import get_db
from app.models.user import User
from app.utils.jwt import create_access_token
from app.schemas.auth import LoginRequest
from app.utils.password import verify_password

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

fake_users = [
    {
        "id": 1,
        "username": "shourya",
        "password" : "$argon2id$v=19$m=65536,t=3,p=4$XDd8htRTC/tsPgZN2U0Ivw$ezYokiLqSsnzGLr51mjywzkR0NgUaS8/DheN8FbSu10"
    },
    {
        "id": 2,
        "username": "admin",
        "password" : "$argon2id$v=19$m=65536,t=3,p=4$R2a8sH1xMs+l/J/t/8YPGQ$LaXNfhXzTRNf/hYEIdzjWsuw87pb/698N95/DLLTwMo"
    }
]

@router.post("/login")
def login(
    user_data: LoginRequest,
    db: session = Depends(get_db)
    ):

    user = db.query(User).filter(
        User.username == user_data.username
    ).first()

    if not user:
        HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )

    if not verify_password(
        user_data.password,
        user.hashed_password
    ):

                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Incorrect username or password"
                )

    if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User account is inactivate"
            )

    access_token = create_access_token({
        "sub": str(user.id),
        "username": str(user.username)
})

    return {
        "access_token": access_token,
        "token_type": "bearer"
}
