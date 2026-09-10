from typing import List, Dict, Optional
from fastapi import FastAPI, Depends, HTTPException, Header, status
from pydantic import BaseModel, Field, EmailStr

app = FastAPI(title="Complete FastApi and Depends Project")

# IN-MEMORY DATABASE
USERS_DB: Dict[str, dict] ={
    "token-admin": {
        "id": 1,
        "username": "admin_user",
        "role": "admin"
    },
    "token-dev": {
        "id": 2,
        "username": "dev_user",
        "role": "developer"
    },
}

TASKS_DB: Dict[int, dict] = {
    1: {
        "id": 1,
        "title": "Setup FastAPI Architecture",
        "description": "Structure routers, models, and dependencies",
        "priority": 1,
        "is_completed": False,
        "assigned_to": "admin_user",
    },

    2: {
        "id": 2,
        "title": "Implement JWT Auth",
        "description": "Secure all routes using bearer tokens",
        "priority": 2,
        "is_completed": False,
        "assigned_to": "dev_user",
    },
}

task_id_counter = 2

#PYDANTIC _SCEMAS
class TaskBase(BaseModel):
    title: str = Field(..., min_length=3, max_length=60, description="Task Heading")
    description: str = Field(..., min_length=10, max_length=200, description="Task Description")
    priority: int = Field(..., ge=1, le=5, description="Task Priority")

class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=3, max_length=60)
    description: Optional[str] = Field(None, min_length=10, max_length=250)
    priority: Optional[int] = Field(None, ge=1, le=5)
    is_completed: Optional[bool] = None

class TaskResponse(BaseModel):
    