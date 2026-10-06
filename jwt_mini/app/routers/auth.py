from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import session

from app.database import get_db
from app.models.user import User
from app.utils.jwt import create_access_token, create_refresh_token, SECRET_KEY, ALGORITHM
from app.schemas.auth import LoginRequest
from app.utils.password import verify_password
from jose import jwt
from jose.exceptions import JWTError

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
        raise HTTPException(
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
        "username": str(user.username),
        "role": str(user.role)
})
    refresh_token = create_refresh_token({
           "sub": str(user.id),
            "username": str(user.username),
            "role": str(user.role)
    })

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
}


@router.post("/refresh")
def refresh_access_token(refresh_token: str):

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid refresh token"
    )

    try:
        payload = jwt.decode(
            refresh_token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        user_id = payload.get("sub")
        username = payload.get("username")
        role = payload.get("role")
        token_type = payload.get("type")

        if (
            user_id is None
            or username is None
            or role is None
            or token_type != "refresh"
        ):
            raise credentials_exception

    except JWTError:
        raise credentials_exception

    new_access_token = create_access_token({
        "sub": user_id,
        "username": username,
        "role": role
    })

    return {
        "access_token": new_access_token,
        "token_type": "bearer"
    }
             
