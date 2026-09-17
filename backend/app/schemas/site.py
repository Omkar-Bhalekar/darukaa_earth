from pydantic import BaseModel
from typing import Any, Dict, List
from uuid import UUID
from datetime import date, datetime

class SiteCreate(BaseModel):
    name: str
    geojson: Dict[str, Any]
    ecosystem_type: str
    monitoring_start_date: date

class SiteResponse(BaseModel):
    id: UUID
    name: str
    geojson: Dict[str, Any]
    area_hectares: float
    ecosystem_type: str
    monitoring_start_date: date
    created_at: datetime
    project_id: UUID
    
    model_config = {"from_attributes": True}

class SiteGeoJSON(BaseModel):
    type: str = "FeatureCollection"
    features: List[Dict[str, Any]]
