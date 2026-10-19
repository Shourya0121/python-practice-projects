from datetime import datetime, timezone
from app.database import Base
from sqlalchemy import Column, Integer, String, DateTime




class RevokedToken(Base):
    __tablename__ = "revoked_tokens"

    id = Column(Integer, primary_key=True, index=True)
    token = Column(String(768), unique=True, nullable=False)
    token_type = Column(String(20), nullable=False)
    family_id = Column(String(100), nullable=True)

    revoked_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )



class RevokedFamily(Base):
    __tablename__ = "revoked_families"

    id = Column(Integer, primary_key=True, index=True)
    family_id = Column(String(100), unique=True, nullable=False)
    revoked_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )