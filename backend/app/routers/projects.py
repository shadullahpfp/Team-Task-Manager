from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.models import domain as models
from app.schemas import dto as schemas
from app.database import get_db
from app.core import auth

router = APIRouter(prefix="/projects", tags=["projects"])

@router.post("/", response_model=schemas.Project)
def create_project(
    project: schemas.ProjectCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.require_admin)
):
    db_project = models.Project(**project.model_dump(), created_by=current_user.id)
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project

@router.get("/", response_model=List[schemas.Project])
def get_projects(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    if current_user.role == models.Role.ADMIN.value:
        return db.query(models.Project).all()
    return current_user.projects

@router.post("/{project_id}/members/{user_id}")
def add_project_member(
    project_id: int,
    user_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.require_admin)
):
    project = db.query(models.Project).filter(models.Project.id == project_id).first()
    user = db.query(models.User).filter(models.User.id == user_id).first()
    
    if not project or not user:
        raise HTTPException(status_code=404, detail="Project or User not found")
        
    if user not in project.members:
        project.members.append(user)
        db.commit()
        
    return {"message": "User added to project"}
