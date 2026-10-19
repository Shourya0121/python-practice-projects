from fastapi import APIRouter, Depends
from app.api.deps import get_current_settings
from app.core.config import Settings

router = APIRouter()


@router.get("/token-info")
def get_token_config(settings: Settings = Depends(get_current_settings)):
    return {
        "token_lifespan_minutes": settings.ACCESS_TOKEN_EXPIRE_MINUTES,
        "secret_configured": bool(settings.SECRET_KEY),
        "secret_prefix": settings.SECRET_KEY[:3] + "..." if settings.SECRET_KEY else None,
    }