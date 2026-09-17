from pydantic import BaseModel
from typing import List, Optional
from uuid import UUID
from datetime import datetime

class ProjectCreate(BaseModel):
    name: str
    description: Optional[str] = None
    project_type: str
    tags: Optional[List[str]] = []

class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    project_type: Optional[str] = None
    tags: Optional[List[str]] = None

class ProjectResponse(BaseModel):
    id: UUID
    name: str
    description: Optional[str] = None
    project_type: str
    tags: List[str]
    site_count: int
    created_at: datetime
    
    model_config = {"from_attributes": True}

class ProjectListResponse(BaseModel):
    data: List[ProjectResponse]
