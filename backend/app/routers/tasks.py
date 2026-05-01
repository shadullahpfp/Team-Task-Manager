from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from app.models import domain as models
from app.schemas import dto as schemas
from app.database import get_db
from app.core import auth

router = APIRouter(prefix="/tasks", tags=["tasks"])

@router.post("/", response_model=schemas.Task)
def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db), current_user: models.User = Depends(auth.require_admin)):
    new_task = models.Task(**task.model_dump())
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

@router.get("/", response_model=List[schemas.Task])
def get_tasks(
    status: Optional[str] = None,
    project_id: Optional[int] = None,
    user_id: Optional[int] = None,
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(auth.get_current_user)
):
    query = db.query(models.Task)
    
    if current_user.role != models.Role.ADMIN.value:
        query = query.filter(models.Task.assignee_id == current_user.id)
    elif user_id:
        query = query.filter(models.Task.assignee_id == user_id)
        
    if status:
        query = query.filter(models.Task.status == status)
        
    if project_id:
        query = query.filter(models.Task.project_id == project_id)
        
    return query.all()

@router.get("/dashboard")
def get_dashboard_stats(db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    query = db.query(models.Task)
    if current_user.role != models.Role.ADMIN.value:
        query = query.filter(models.Task.assignee_id == current_user.id)
        
    tasks = query.all()
    now = datetime.utcnow()
    
    return {
        "total": len(tasks),
        "todo": len([t for t in tasks if t.status == models.TaskStatus.TODO.value]),
        "in_progress": len([t for t in tasks if t.status == models.TaskStatus.IN_PROGRESS.value]),
        "done": len([t for t in tasks if t.status == models.TaskStatus.DONE.value]),
        "overdue": len([t for t in tasks if t.status != models.TaskStatus.DONE.value and t.due_date and t.due_date < now])
    }

@router.patch("/{task_id}", response_model=schemas.Task)
def update_task(task_id: int, update: schemas.TaskUpdate, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
        
    if current_user.role != models.Role.ADMIN.value and task.assignee_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to update this task")

    update_data = update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        if key == "status" and hasattr(value, "value"):
            setattr(task, key, value.value)
        else:
            setattr(task, key, value)
        
    db.commit()
    db.refresh(task)
    return task

@router.delete("/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(auth.require_admin)):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(task)
    db.commit()
    return {"success": True}
