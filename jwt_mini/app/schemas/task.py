from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None

#DATA CAN CLIENT CAN SEND  WHEN CREATING AN TASK

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None

# DATA API WILL RETURN TO THE CLIENT
class TaskResponse(BaseModel):
    id: int
    title: str
    Description: Optional[str] = None
    completed: bool
    owner_id: int
    created_at: datetime

    class config:
        from_attribute = True