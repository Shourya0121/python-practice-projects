from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError

from app.utils.jwt import SECRET_KEY, ALGORITHM

oauth_scheme = OAuth2PasswordBearer(
    tokenUrl="auth/login"
)


def get_current_user(token: str = Depends(oauth_scheme)):

    CredientialErrors = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try: 
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
    )

        user_id = payload.get("sub")
        username = payload.get("username")

        if user_id is None or username is None:
            raise CredientialErrors

    except JWTError:
        raise CredientialErrors

    return {
    "id": user_id,
    "username" :username
}
