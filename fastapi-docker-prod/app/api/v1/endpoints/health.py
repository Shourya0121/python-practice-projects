from fastapi import APIRouter, Depends
from app.api.deps import get_current_settings
from app.core.config import Settings
from app.schemas.health import HealthCheckResponse

router = APIRouter()


@router.get("/health", response_model=HealthCheckResponse)
def check_health(settings: Settings = Depends(get_current_settings)):
    return HealthCheckResponse(
        status="healthy",
        environment=settings.ENVIRONMENT,
        version=settings.VERSION,
        debug_mode=settings.DEBUG,
    )