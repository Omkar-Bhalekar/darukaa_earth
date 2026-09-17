from datetime import date
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel


class MetricResponse(BaseModel):
    id: UUID
    site_id: UUID
    recorded_date: date
    canopy_cover_pct: Optional[float] = None
    ndvi: Optional[float] = None
    carbon_tco2e: Optional[float] = None
    biodiversity_index: Optional[float] = None

    model_config = {"from_attributes": True}


class MetricsListResponse(BaseModel):
    data: List[MetricResponse]
