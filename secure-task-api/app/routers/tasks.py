from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.security import get_current_user
from app.db.session import get_db
from app.models.task import Task
from app.models.user import User
from app.schemas.task import TaskCreate, TaskResponse, TaskUpdate


router = APIRouter(
    prefix="/tasks",
    tags=["tasks"]
)

CurrentUser = Annotated[User, Depends(get_current_user)]
DatabaseSession = Annotated[Session, Depends(get_db)]

@router.post(
    "/",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
)

def create_task(
    task_data: TaskCreate,
    current_user: CurrentUser,
    db: DatabaseSession
): 

    task = Task(
        title=task_data.title,
        description=task_data.description,
        owner_id=current_user.id
    )

    db.add(task)
    db.commit()
    db.refresh(task)

    return task

@router.get("/", response_model=list[TaskResponse])
def get_my_tasks(
    current_user: CurrentUser,
    db: DatabaseSession
):
    statement = (
        select(Task)
        .where(Task.owner_id == current_user.id)
        .order_by(Task.id.desc())
    )

    return db.scalars(statement).all()

@router.get("/{task_id}", response_model=TaskResponse)
def get_task(
    task_id: int,
    current_user: CurrentUser,
    db: DatabaseSession
):
    task = db.scalar(
        select(Task).where(
            Task.id == task_id,
            Task.owner_id == current_user.id,
        )
    )

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    return task

@router.patch("/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: int,
    task_data: TaskUpdate,
    current_user: CurrentUser,
    db: DatabaseSession
):
    task = db.scalar(
        select(Task).where(
            Task.id == task_id,
            Task.owner_id == current_user.id,
        )
    )

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    updates = task_data.model_dump(exclude_unset=True)

    for field, value in updates.items():
        setattr(task, field, value)

    db.commit()
    db.refresh(task)

    return task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: int,
    current_user: CurrentUser,
    db: DatabaseSession
):
    task = db.scalar(
        select(Task).where(
            Task.id == task_id,
            Task.owner_id == current_user.id,
        )
    )

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    db.delete(task)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)