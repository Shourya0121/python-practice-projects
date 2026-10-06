from jose import jwt
from datetime import datetime, timedelta, timezone

SECRET_KEY = "my-super-secret-key"
ALGORITHM  = "HS256"

def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(minutes=30)

    to_encode.update({
       "exp": expire,
       "type": "access"
    })

    return jwt.encode(
       to_encode,
       SECRET_KEY,
       algorithm=ALGORITHM
    )

def create_refresh_token(data: dict):
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(days=7)

    to_encode.update({
        "exp": expire,
        "type": "refresh"
    })
    return jwt.encode(
           to_encode,
           SECRET_KEY,
           algorithm=ALGORITHM
        )