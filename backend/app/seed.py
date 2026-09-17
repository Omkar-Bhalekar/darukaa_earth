import asyncio
import math
import random
from datetime import date
from dateutil.relativedelta import relativedelta
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import engine, Base
from app.models.user import User
from app.models.project import Project
from app.models.site import Site
from app.models.metric import SiteMetric
from app.auth.security import hash_password
from sqlalchemy import func
import json

def generate_polygon(lat, lon):
    s = random.uniform(0.006, 0.02)
    return {
        "type": "Polygon",
        "coordinates": [[
            [lon, lat],
            [lon + s, lat],
            [lon + s, lat + s],
            [lon, lat + s],
            [lon, lat]
        ]]
    }

async def seed():
    from app.database import AsyncSessionLocal
    async with AsyncSessionLocal() as db:
        # Demo User
        res = await db.execute(select(User).filter(User.email == "demo@darukaa.earth"))
        user = res.scalar_one_or_none()
        if not user:
            user = User(
                email="demo@darukaa.earth",
                hashed_password=hash_password("demo1234"),
                name="Demo Admin"
            )
            db.add(user)
            await db.commit()
            await db.refresh(user)
            print("Created demo user")
        else:
            print("Demo user already exists")

        projects_data = [
            {"name": "Western Ghats Reforestation Initiative", "type": "carbon", "lat": 12.5, "lon": 75.5},
            {"name": "Sundarbans Mangrove Restoration", "type": "biodiversity", "lat": 21.9, "lon": 89.2},
            {"name": "Cerrado Savanna Biodiversity Corridor", "type": "biodiversity", "lat": -14.2, "lon": -47.5}
        ]

        for p_data in projects_data:
            res = await db.execute(select(Project).filter(Project.name == p_data["name"]))
            if not res.scalar_one_or_none():
                proj = Project(
                    owner_id=user.id,
                    name=p_data["name"],
                    description=f"Demo project for {p_data['name']}",
                    project_type=p_data["type"],
                    tags=["demo", p_data["type"]]
                )
                db.add(proj)
                await db.commit()
                await db.refresh(proj)
                print(f"Created project: {proj.name}")

                for i in range(1, 4):
                    lat = p_data["lat"] + random.uniform(-0.1, 0.1)
                    lon = p_data["lon"] + random.uniform(-0.1, 0.1)
                    geojson = generate_polygon(lat, lon)
                    geojson_str = json.dumps(geojson)
                    
                    area_res = await db.execute(select(func.ST_Area(func.ST_GeomFromGeoJSON(geojson_str).cast(func.Geography())) / 10000))
                    area_hectares = area_res.scalar_one()

                    site = Site(
                        project_id=proj.id,
                        name=f"Site {i} - {proj.name[:10]}",
                        ecosystem_type="Forest",
                        monitoring_start_date=date.today() - relativedelta(months=36),
                        geom=func.ST_GeomFromGeoJSON(geojson_str),
                        area_hectares=area_hectares
                    )
                    db.add(site)
                    await db.commit()
                    await db.refresh(site)

                    start_date = site.monitoring_start_date
                    for m in range(36):
                        m_date = start_date + relativedelta(months=m)
                        L = 85
                        k = 0.15
                        t0 = 18
                        canopy = L / (1 + math.exp(-k*(m-t0))) + random.gauss(0, 2)
                        ndvi = 0.3 + 0.4*(m/36) + 0.05*math.sin(2*math.pi*m/12) + random.gauss(0, 0.03)
                        carbon = 5 + (10 * (m/36)) + random.gauss(0, 0.5)

                        bio_index = 0.3
                        if m >= 18:
                            bio_index = 0.7
                        elif m >= 12:
                            bio_index = 0.5
                        elif m >= 6:
                            bio_index = 0.4
                        bio_index += random.gauss(0, 0.05)

                        metric = SiteMetric(
                            site_id=site.id,
                            recorded_date=m_date,
                            canopy_cover_pct=max(0, min(100, canopy)),
                            ndvi=max(0, min(1, ndvi)),
                            carbon_tco2e=max(0, carbon),
                            biodiversity_index=max(0, min(1, bio_index))
                        )
                        db.add(metric)
                    await db.commit()

if __name__ == "__main__":
    asyncio.run(seed())
