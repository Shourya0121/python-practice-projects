from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import session

from app.database import get_db
from app.models.user import User

from app.utils.jwt import (
    create_access_token,
    create_refresh_token,
    hash_password,
    verify_password,
    revoke_token,
    is_token_revoked,
    revoke_family,
    is_family_revoked,
)
from app.config import JWT_SECRET_KEY, JWT_ALGORITHM
from app.schemas.auth import LoginRequest, RegisterRequest
from jose import jwt
from jose.exceptions import JWTError
from app.dependencies.auth import oauth_scheme



router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)
@router.post("/register")
def register(
     user_data: RegisterRequest,
     db: session = Depends(get_db)
):

     existing_user = (
          db.query(User)
          .filter(User.username == user_data.username)
          .first()
     )

     if existing_user:
          raise HTTPException(
               status_code=status.HTTP_400_BAD_REQUEST,
               detail="Username already Exists"
          )

     new_user = User(
          username=user_data.username,
          display_name=user_data.display_name,
          hashed_password=hash_password(user_data.password),
          role="user",
          is_active=True
     )

     db.add(new_user)
     db.commit()
     db.refresh(new_user)

     return {
          "message": "This user successfully registered",
          "user":{
               "user_id": new_user.id,
               "username": new_user.username,
               "display_name": new_user.display_name,
               "role": new_user.role,
               "is_active": new_user.is_active
          }
     }

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
def refresh_access_token(
    refresh_token: str,
    db: session = Depends(get_db)
):

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid refresh token"
    )

    try:
        payload = jwt.decode(
            refresh_token,
            JWT_SECRET_KEY,
            algorithms=[JWT_ALGORITHM]
        )

        if is_token_revoked(db, refresh_token):
            family_id = payload.get("family_id")

            if family_id:
                 revoke_family(db, family_id)

            raise HTTPException(
                status_code=401,
                detail="Refresh token reuse detected. Token family has been revoked"
        )

        token_type = payload.get("type")

        if token_type != "refresh":
              raise HTTPException(
                    status_code=401,
                    detail="Invalid refresh token")

        user_id = payload.get("sub")
        username = payload.get("username")
        role = payload.get("role")
        token_type = payload.get("type")
        family_id = payload.get("family_id")

        if family_id and is_family_revoked(db, family_id):
             raise HTTPException(
                  status_code=401,
                  detail="Token family has been revoked. Please login again."
             )

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
    new_refresh_token = create_refresh_token(
    {
         "sub": user_id,
         "username": username,
         "role": role 
    },
    family_id=family_id
    )
        

    revoke_token(
    db,
    refresh_token,
    "refresh",
    family_id
)

    return {
        "access_token": new_access_token,
        "refresh_token": new_refresh_token,
        "token_type": "bearer"
    }

@router.post("/logout")
def logout(
    token: str = Depends(oauth_scheme),
    refresh_token: str = "",
    db: session = Depends(get_db)
):
      revoke_token(
    db,
    token,
    "access"
)
      revoke_token(
    db,
    refresh_token,
    "refresh"
)

      return {
            "message": "Successfully logged out"
      }
             
