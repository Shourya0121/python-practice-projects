from pydantic import BaseModel


class HealthCheckResponse(BaseModel):
    status: str
    environment: str
    version: str
    debug_mode: bool