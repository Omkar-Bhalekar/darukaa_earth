import json
import uuid
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.dependencies import get_current_user
from app.database import get_db
from app.models.project import Project
from app.models.site import Site
from app.models.user import User
from app.schemas.site import SiteCreate, SiteGeoJSON, SiteResponse

router = APIRouter(prefix="/api", tags=["sites"])


@router.post("/projects/{project_id}/sites", response_model=SiteResponse)
async def create_site(
    project_id: uuid.UUID,
    site_in: SiteCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    # Verify project ownership
    proj_res = await db.execute(
        select(Project).filter(
            Project.id == project_id,
            Project.owner_id == current_user.id,
            Project.is_deleted.is_(False),
        )
    )
    if not proj_res.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="Project not found")

    geojson_str = json.dumps(site_in.geojson)

    # Calculate area and convert to geography using PostGIS
    area_res = await db.execute(
        select(
            func.ST_Area(func.ST_GeomFromGeoJSON(geojson_str).cast(func.Geography()))
            / 10000
        )
    )
    area_hectares = area_res.scalar_one()

    new_site = Site(
        project_id=project_id,
        name=site_in.name,
        ecosystem_type=site_in.ecosystem_type,
        monitoring_start_date=site_in.monitoring_start_date,
        geom=func.ST_GeomFromGeoJSON(geojson_str),
        area_hectares=area_hectares,
    )
    db.add(new_site)
    await db.commit()
    await db.refresh(new_site)

    # Fetch it back with geojson
    fetch_res = await db.execute(
        select(Site, func.ST_AsGeoJSON(Site.geom).label("geojson")).filter(
            Site.id == new_site.id
        )
    )
    site_obj, gjson_str = fetch_res.first()

    return SiteResponse(
        id=site_obj.id,
        name=site_obj.name,
        geojson=json.loads(gjson_str),
        area_hectares=site_obj.area_hectares,
        ecosystem_type=site_obj.ecosystem_type,
        monitoring_start_date=site_obj.monitoring_start_date,
        created_at=site_obj.created_at,
        project_id=site_obj.project_id,
    )


@router.get("/projects/{project_id}/sites", response_model=List[SiteResponse])
async def list_sites(
    project_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    proj_res = await db.execute(
        select(Project).filter(
            Project.id == project_id,
            Project.owner_id == current_user.id,
            Project.is_deleted.is_(False),
        )
    )
    if not proj_res.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="Project not found")

    result = await db.execute(
        select(Site, func.ST_AsGeoJSON(Site.geom).label("geojson")).filter(
            Site.project_id == project_id
        )
    )
    out = []
    for site_obj, gjson_str in result.all():
        out.append(
            SiteResponse(
                id=site_obj.id,
                name=site_obj.name,
                geojson=json.loads(gjson_str),
                area_hectares=site_obj.area_hectares,
                ecosystem_type=site_obj.ecosystem_type,
                monitoring_start_date=site_obj.monitoring_start_date,
                created_at=site_obj.created_at,
                project_id=site_obj.project_id,
            )
        )
    return out


@router.get("/sites/all-geojson", response_model=SiteGeoJSON)
async def get_all_sites_geojson(
    current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Site, func.ST_AsGeoJSON(Site.geom).label("geojson"))
        .join(Project, Site.project_id == Project.id)
        .filter(Project.owner_id == current_user.id, Project.is_deleted.is_(False))
    )
    features = []
    for site_obj, gjson_str in result.all():
        geometry = json.loads(gjson_str)
        features.append(
            {
                "type": "Feature",
                "geometry": geometry,
                "properties": {
                    "id": str(site_obj.id),
                    "name": site_obj.name,
                    "ecosystem_type": site_obj.ecosystem_type,
                    "project_id": str(site_obj.project_id),
                },
            }
        )
    return SiteGeoJSON(type="FeatureCollection", features=features)


@router.get("/sites/{site_id}", response_model=SiteResponse)
async def get_site(
    site_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Site, func.ST_AsGeoJSON(Site.geom).label("geojson"))
        .join(Project, Site.project_id == Project.id)
        .filter(
            Site.id == site_id,
            Project.owner_id == current_user.id,
            Project.is_deleted.is_(False),
        )
    )
    row = result.first()
    if not row:
        raise HTTPException(status_code=404, detail="Site not found")
    site_obj, gjson_str = row
    return SiteResponse(
        id=site_obj.id,
        name=site_obj.name,
        geojson=json.loads(gjson_str),
        area_hectares=site_obj.area_hectares,
        ecosystem_type=site_obj.ecosystem_type,
        monitoring_start_date=site_obj.monitoring_start_date,
        created_at=site_obj.created_at,
        project_id=site_obj.project_id,
    )


@router.delete("/sites/{site_id}")
async def delete_site(
    site_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Site)
        .join(Project, Site.project_id == Project.id)
        .filter(
            Site.id == site_id,
            Project.owner_id == current_user.id,
            Project.is_deleted.is_(False),
        )
    )
    site_obj = result.scalar_one_or_none()
    if not site_obj:
        raise HTTPException(status_code=404, detail="Site not found")
    await db.delete(site_obj)
    await db.commit()
    return {"detail": "Site deleted"}
