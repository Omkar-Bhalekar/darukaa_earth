from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload
from app.database import get_db
from app.models.user import User
from app.models.project import Project
from app.models.site import Site
from app.schemas.project import ProjectCreate, ProjectUpdate, ProjectResponse
from app.auth.dependencies import get_current_user
import uuid
from typing import List

router = APIRouter(prefix="/api/projects", tags=["projects"])

@router.get("", response_model=List[ProjectResponse])
async def list_projects(current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Project, func.count(Site.id).label("site_count"))
        .outerjoin(Site, Project.id == Site.project_id)
        .filter(Project.owner_id == current_user.id, Project.is_deleted.is_(False))
        .group_by(Project.id)
    )
    rows = result.all()
    out = []
    for proj, count in rows:
        p_dict = {
            "id": proj.id,
            "name": proj.name,
            "description": proj.description,
            "project_type": proj.project_type,
            "tags": proj.tags,
            "site_count": count,
            "created_at": proj.created_at
        }
        out.append(ProjectResponse(**p_dict))
    return out

@router.post("", response_model=ProjectResponse)
async def create_project(project_in: ProjectCreate, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    new_proj = Project(
        owner_id=current_user.id,
        name=project_in.name,
        description=project_in.description,
        project_type=project_in.project_type,
        tags=project_in.tags or []
    )
    db.add(new_proj)
    await db.commit()
    await db.refresh(new_proj)
    
    p_dict = {
        "id": new_proj.id,
        "name": new_proj.name,
        "description": new_proj.description,
        "project_type": new_proj.project_type,
        "tags": new_proj.tags,
        "site_count": 0,
        "created_at": new_proj.created_at
    }
    return ProjectResponse(**p_dict)

@router.get("/{project_id}", response_model=ProjectResponse)
async def get_project(project_id: uuid.UUID, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Project, func.count(Site.id).label("site_count"))
        .outerjoin(Site, Project.id == Site.project_id)
        .filter(Project.id == project_id, Project.owner_id == current_user.id, Project.is_deleted.is_(False))
        .group_by(Project.id)
    )
    row = result.first()
    if not row:
        raise HTTPException(status_code=404, detail="Project not found")
    proj, count = row
    p_dict = {
        "id": proj.id,
        "name": proj.name,
        "description": proj.description,
        "project_type": proj.project_type,
        "tags": proj.tags,
        "site_count": count,
        "created_at": proj.created_at
    }
    return ProjectResponse(**p_dict)

@router.put("/{project_id}", response_model=ProjectResponse)
async def update_project(project_id: uuid.UUID, project_in: ProjectUpdate, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Project).filter(Project.id == project_id, Project.owner_id == current_user.id, Project.is_deleted.is_(False)))
    proj = result.scalar_one_or_none()
    if not proj:
        raise HTTPException(status_code=404, detail="Project not found")
    
    if project_in.name is not None:
        proj.name = project_in.name
    if project_in.description is not None:
        proj.description = project_in.description
    if project_in.project_type is not None:
        proj.project_type = project_in.project_type
    if project_in.tags is not None:
        proj.tags = project_in.tags
        
    await db.commit()
    await db.refresh(proj)
    
    site_count_res = await db.execute(select(func.count(Site.id)).filter(Site.project_id == project_id))
    count = site_count_res.scalar_one()
    
    p_dict = {
        "id": proj.id,
        "name": proj.name,
        "description": proj.description,
        "project_type": proj.project_type,
        "tags": proj.tags,
        "site_count": count,
        "created_at": proj.created_at
    }
    return ProjectResponse(**p_dict)

@router.delete("/{project_id}")
async def delete_project(project_id: uuid.UUID, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Project).filter(Project.id == project_id, Project.owner_id == current_user.id, Project.is_deleted.is_(False)))
    proj = result.scalar_one_or_none()
    if not proj:
        raise HTTPException(status_code=404, detail="Project not found")
    proj.is_deleted = True
    await db.commit()
    return {"detail": "Project deleted"}
