from app.core.config import Settings, get_settings


def get_current_settings() -> Settings:
    """Dependency helper to supply cached application settings."""
    return get_settings()