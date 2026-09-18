import asyncio
import json
import random
from datetime import date

from dateutil.relativedelta import relativedelta
from sqlalchemy import func, select

from app.auth.security import hash_password
from app.metrics_synth import synthetic_monthly_metrics
from app.models.project import Project
from app.models.site import Site
from app.models.user import User


def generate_polygon(lat, lon):
    s = random.uniform(0.006, 0.02)
    return {
        "type": "Polygon",
        "coordinates": [
            [[lon, lat], [lon + s, lat], [lon + s, lat + s], [lon, lat + s], [lon, lat]]
        ],
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
                name="Demo Admin",
            )
            db.add(user)
            await db.commit()
            await db.refresh(user)
            print("Created demo user")
        else:
            print("Demo user already exists")

        projects_data = [
            {
                "name": "Western Ghats Reforestation Initiative",
                "type": "carbon",
                "lat": 12.5,
                "lon": 75.5,
            },
            {
                "name": "Sundarbans Mangrove Restoration",
                "type": "biodiversity",
                "lat": 21.9,
                "lon": 89.2,
            },
            {
                "name": "Cerrado Savanna Biodiversity Corridor",
                "type": "biodiversity",
                "lat": -14.2,
                "lon": -47.5,
            },
        ]

        for p_data in projects_data:
            res = await db.execute(
                select(Project).filter(Project.name == p_data["name"])
            )
            if not res.scalar_one_or_none():
                proj = Project(
                    owner_id=user.id,
                    name=p_data["name"],
                    description=f"Demo project for {p_data['name']}",
                    project_type=p_data["type"],
                    tags=["demo", p_data["type"]],
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

                    area_res = await db.execute(
                        select(
                            func.ST_Area(
                                func.ST_GeomFromGeoJSON(geojson_str).cast(
                                    func.Geography()
                                )
                            )
                            / 10000
                        )
                    )
                    area_hectares = area_res.scalar_one()

                    site = Site(
                        project_id=proj.id,
                        name=f"Site {i} - {proj.name[:10]}",
                        ecosystem_type="Forest",
                        monitoring_start_date=date.today() - relativedelta(months=36),
                        geom=func.ST_GeomFromGeoJSON(geojson_str),
                        area_hectares=area_hectares,
                    )
                    db.add(site)
                    await db.commit()
                    await db.refresh(site)

                    start_date = site.monitoring_start_date
                    db.add_all(synthetic_monthly_metrics(site.id, start_date))
                    await db.commit()


if __name__ == "__main__":
    asyncio.run(seed())
