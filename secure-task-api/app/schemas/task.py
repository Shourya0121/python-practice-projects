from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class TaskCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    description: str | None = None

class TaskUpdate(BaseModel):
    title: str = Field(default=None, min_length=1, max_length=200)
    description: str | None = None
    is_completed: bool | None = None


class TaskResponse(BaseModel):
    id: int
    title: str
    description: str | None
    is_completed: bool
    owner_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)