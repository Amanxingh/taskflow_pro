from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate, TaskRead, TaskPage
from app.services.task_service import create_task, apply_task_update

router = APIRouter()


@router.get("/health", tags=["Health"])
def health_check():
    return {"status": "ok"}


@router.post("/tasks", response_model=TaskRead, status_code=status.HTTP_201_CREATED, tags=["Tasks"])
def create_new_task(payload: TaskCreate, db: Session = Depends(get_db)):
    return create_task(db, payload)


@router.get("/tasks", response_model=TaskPage, tags=["Tasks"])
def list_tasks(
    q: str | None = Query(default=None, description="Search title and description"),
    completed: bool | None = None,
    priority: str | None = Query(default=None, pattern="^(low|medium|high)$"),
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    stmt = select(Task)
    if q:
        search = f"%{q.strip()}%"
        stmt = stmt.where(or_(Task.title.ilike(search), Task.description.ilike(search)))
    if completed is not None:
        stmt = stmt.where(Task.completed == completed)
    if priority:
        stmt = stmt.where(Task.priority == priority)
    total = len(db.scalars(stmt).all())
    items = db.scalars(stmt.order_by(Task.created_at.desc()).offset(skip).limit(limit)).all()
    return {"items": items, "total": total, "skip": skip, "limit": limit}


@router.get("/tasks/{task_id}", response_model=TaskRead, tags=["Tasks"])
def get_task(task_id: int, db: Session = Depends(get_db)):
    task = db.get(Task, task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.patch("/tasks/{task_id}", response_model=TaskRead, tags=["Tasks"])
def update_task(task_id: int, payload: TaskUpdate, db: Session = Depends(get_db)):
    task = db.get(Task, task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return apply_task_update(db, task, payload)


@router.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Tasks"])
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = db.get(Task, task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(task)
    db.commit()
    return None
