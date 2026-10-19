from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.api.v1.router import api_router
from app.core.config import get_settings

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Runs when container initializes
    print(f"[STARTUP] Initializing {settings.PROJECT_NAME} (v{settings.VERSION})")
    print(f"[STARTUP] Running in '{settings.ENVIRONMENT}' mode on port {settings.PORT}.")
    yield
    # Runs when container receives termination signal (docker stop)
    print(f"[SHUTDOWN] Gracefully terminating {settings.PROJECT_NAME}.")


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url=f"{settings.API_V1_STR}/docs",
    redoc_url=f"{settings.API_V1_STR}/redoc",
    lifespan=lifespan,
)

# Mount all /api/v1 routes
app.include_router(api_router, prefix=settings.API_V1_STR)