from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from app.utils.jwt import is_token_revoked
from app.database import get_db
from sqlalchemy.orm import Session

from app.config import JWT_SECRET_KEY, JWT_ALGORITHM

oauth_scheme = OAuth2PasswordBearer(
    tokenUrl="auth/login"
)


def get_current_user(
    token: str = Depends(oauth_scheme),
    db: Session = Depends(get_db)
):

    CredientialErrors = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try: 
        payload = jwt.decode(
            token,
            JWT_SECRET_KEY,
            algorithms=[JWT_ALGORITHM]
    )

        if is_token_revoked(db, token):
            raise CredientialErrors

        user_id = payload.get("sub")
        username = payload.get("username")
        role = payload.get("role")
        token = payload.get("type")

        if(

        user_id is None
        or username is None
        or role is None 
        or token != "access"
        ):
            raise CredientialErrors

    except JWTError:
        raise CredientialErrors

    return {
    "id": user_id,
    "username":username,
    "role": role
}

def get_current_admin(
    current_user: dict = Depends(get_current_user)
):
    if current_user["role"] != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )

    return current_user
