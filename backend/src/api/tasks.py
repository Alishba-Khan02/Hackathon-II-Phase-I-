from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from ..models import Task, User
from ..database import get_session
from ..services.auth import get_current_user
from ..services import tasks as task_service

router = APIRouter()

# Create Task
@router.post("/tasks/", response_model=Task, status_code=status.HTTP_201_CREATED)
def create_task_endpoint(
    task: Task,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    return task_service.create_task(session, task.title, current_user, task.description)

# Get all tasks
@router.get("/tasks/", response_model=List[Task])
def get_tasks_endpoint(session: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    return task_service.get_tasks(session, current_user)

# Get single task
@router.get("/tasks/{task_id}", response_model=Task)
def get_task_endpoint(task_id: int, session: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    task = task_service.get_task(session, task_id, current_user)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

# Update Task (PATCH for frontend Save/Edit)
@router.patch("/tasks/{task_id}", response_model=Task)
def update_task_endpoint(
    task_id: int,
    task: Task,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    updated_task = task_service.update_task(
        session,
        task_id,
        current_user,
        title=task.title,
        description=task.description,
        completed=task.completed if task.completed is not None else None,
    )
    if not updated_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return updated_task

# Delete Task
@router.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task_endpoint(task_id: int, session: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    if not task_service.delete_task(session, task_id, current_user):
        raise HTTPException(status_code=404, detail="Task not found")
    return

# Complete Task
@router.patch("/tasks/{task_id}/complete", response_model=Task)
def complete_task_endpoint(task_id: int, session: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    completed_task = task_service.update_task(session, task_id, current_user, completed=True)
    if not completed_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return completed_task

# Uncomplete Task
@router.patch("/tasks/{task_id}/uncomplete", response_model=Task)
def uncomplete_task_endpoint(task_id: int, session: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    uncompleted_task = task_service.update_task(session, task_id, current_user, completed=False)
    if not uncompleted_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return uncompleted_task
