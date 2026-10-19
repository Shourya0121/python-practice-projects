from datetime import datetime, timedelta, timezone
from uuid import uuid4

from jose import jwt
from sqlalchemy.orm import Session
from pwdlib import PasswordHash

from app.config import JWT_SECRET_KEY, JWT_ALGORITHM
from app.models.revoked_token import RevokedToken, RevokedFamily


# PASSWORD HASHING


password_hash = PasswordHash.recommended()


def hash_password(password: str) -> str:
    return password_hash.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    return password_hash.verify(password, hashed_password)


# JWT TOKEN CREATION


def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(minutes=30)

    to_encode.update({
        "exp": expire,
        "type": "access"
    })

    return jwt.encode(
        to_encode,
        JWT_SECRET_KEY,
        algorithm=JWT_ALGORITHM
    )


def create_refresh_token(
    data: dict,
    family_id: str | None = None
):
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(days=7)

    if family_id is None:
        family_id = str(uuid4())

    to_encode.update({
        "exp": expire,
        "type": "refresh",
        "family_id": family_id
    })

    return jwt.encode(
        to_encode,
        JWT_SECRET_KEY,
        algorithm=JWT_ALGORITHM
    )



# TOKEN BLACKLIST

def revoke_token(
    db: Session,
    token: str,
    token_type: str,
    family_id: str | None = None
):
    existing_token = (
        db.query(RevokedToken)
        .filter(RevokedToken.token == token)
        .first()
    )

    if existing_token:
        return

    revoked_token = RevokedToken(
        token=token,
        token_type=token_type,
        family_id=family_id
    )

    db.add(revoked_token)
    db.commit()


def is_token_revoked(
    db: Session,
    token: str
) -> bool:

    revoked_token = (
        db.query(RevokedToken)
        .filter(RevokedToken.token == token)
        .first()
    )

    return revoked_token is not None



# REFRESH TOKEN FAMILY REVOCATION

def revoke_family(
    db: Session,
    family_id: str
):
    existing_family = (
        db.query(RevokedFamily)
        .filter(RevokedFamily.family_id == family_id)
        .first()
    )

    if existing_family:
        return

    revoked_family = RevokedFamily(
        family_id=family_id
    )

    db.add(revoked_family)
    db.commit()


def is_family_revoked(
    db: Session,
    family_id: str
) -> bool:

    revoked_family = (
        db.query(RevokedFamily)
        .filter(RevokedFamily.family_id == family_id)
        .first()
    )

    return revoked_family is not None