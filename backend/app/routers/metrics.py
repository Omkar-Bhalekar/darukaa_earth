from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.database import get_db
from app.models.user import User
from app.models.site import Site
from app.models.project import Project
from app.models.metric import SiteMetric
from app.schemas.metric import MetricResponse
from app.auth.dependencies import get_current_user
import uuid
from typing import List, Optional
from datetime import date

router = APIRouter(prefix="/api/sites/{site_id}/metrics", tags=["metrics"])

@router.get("", response_model=List[MetricResponse])
async def get_metrics(
    site_id: uuid.UUID,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    # Verify access
    site_res = await db.execute(
        select(Site)
        .join(Project, Site.project_id == Project.id)
        .filter(Site.id == site_id, Project.owner_id == current_user.id, Project.is_deleted.is_(False))
    )
    if not site_res.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="Site not found")

    query = select(SiteMetric).filter(SiteMetric.site_id == site_id).order_by(SiteMetric.recorded_date)
    if start_date:
        query = query.filter(SiteMetric.recorded_date >= start_date)
    if end_date:
        query = query.filter(SiteMetric.recorded_date <= end_date)

    result = await db.execute(query)
    metrics = result.scalars().all()
    return metrics

@router.get("/summary")
async def get_metrics_summary(
    site_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    site_res = await db.execute(
        select(Site)
        .join(Project, Site.project_id == Project.id)
        .filter(Site.id == site_id, Project.owner_id == current_user.id, Project.is_deleted.is_(False))
    )
    if not site_res.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="Site not found")

    # Get latest metric
    latest_res = await db.execute(
        select(SiteMetric)
        .filter(SiteMetric.site_id == site_id)
        .order_by(SiteMetric.recorded_date.desc())
        .limit(1)
    )
    latest = latest_res.scalar_one_or_none()
    
    # Get aggregates
    agg_res = await db.execute(
        select(
            func.sum(SiteMetric.carbon_tco2e).label('total_carbon'),
            func.avg(SiteMetric.ndvi).label('avg_ndvi'),
            func.avg(SiteMetric.canopy_cover_pct).label('avg_canopy'),
            func.avg(SiteMetric.biodiversity_index).label('avg_biodiversity')
        )
        .filter(SiteMetric.site_id == site_id)
    )
    aggs = agg_res.first()

    return {
        "latest": latest,
        "aggregates": {
            "total_carbon_tco2e": aggs.total_carbon if aggs.total_carbon else 0.0,
            "avg_ndvi": aggs.avg_ndvi if aggs.avg_ndvi else 0.0,
            "avg_canopy_cover_pct": aggs.avg_canopy if aggs.avg_canopy else 0.0,
            "avg_biodiversity_index": aggs.avg_biodiversity if aggs.avg_biodiversity else 0.0
        }
    }
