from typing import List, Optional
from sqlmodel import Session, select
from ..models import Task, User

def create_task(session: Session, title: str, user: User, description: Optional[str] = None, completed: bool = False) -> Task:
    task = Task(title=title, description=description, completed=completed, owner_id=user.id)
    session.add(task)
    session.commit()
    session.refresh(task)
    return task

def get_tasks(session: Session, user: User) -> List[Task]:
    return session.exec(select(Task).where(Task.owner_id == user.id)).all()

def get_task(session: Session, task_id: int, user: User) -> Optional[Task]:
    return session.exec(select(Task).where(Task.id == task_id, Task.owner_id == user.id)).first()

def update_task(session: Session, task_id: int, user: User, title: Optional[str] = None, description: Optional[str] = None, completed: Optional[bool] = None) -> Optional[Task]:
    task = get_task(session, task_id, user)
    if task:
        if title is not None:
            task.title = title
        if description is not None:
            task.description = description
        if completed is not None:
            task.completed = completed
        session.add(task)
        session.commit()
        session.refresh(task)
    return task

def delete_task(session: Session, task_id: int, user: User) -> bool:
    task = get_task(session, task_id, user)
    if task:
        session.delete(task)
        session.commit()
        return True
    return False
