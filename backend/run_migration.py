"""
Standalone migration runner for Windows.
Bypasses SQLAlchemy's asyncpg greenlet bridge (which fails with
ProactorEventLoop on Windows + TLS).  Uses asyncpg directly to apply
the exact same DDL that alembic/versions/0001_initial_schema.py defines.
"""
import asyncio
import os
import ssl
import sys

import asyncpg
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))

RAW_URL = os.environ["DATABASE_URL"].replace("postgresql+asyncpg://", "postgresql://")

MIGRATION_SQL = """
-- Enable extensions
CREATE EXTENSION IF NOT EXISTS pgcrypto;
CREATE EXTENSION IF NOT EXISTS postgis;

-- users
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) NOT NULL UNIQUE,
    hashed_password VARCHAR(255) NOT NULL,
    name VARCHAR(255) NOT NULL,
    created_at TIMESTAMPTZ DEFAULT now()
);

-- projects
CREATE TABLE IF NOT EXISTS projects (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    owner_id UUID NOT NULL REFERENCES users(id),
    name VARCHAR(255) NOT NULL,
    description TEXT,
    project_type VARCHAR(50) NOT NULL,
    tags VARCHAR[] NOT NULL DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT now(),
    is_deleted BOOLEAN NOT NULL DEFAULT false
);

-- sites
CREATE TABLE IF NOT EXISTS sites (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id UUID NOT NULL REFERENCES projects(id),
    name VARCHAR(255) NOT NULL,
    geom geography(POLYGON, 4326) NOT NULL,
    area_hectares FLOAT NOT NULL,
    ecosystem_type VARCHAR(100) NOT NULL,
    monitoring_start_date DATE NOT NULL,
    created_at TIMESTAMPTZ DEFAULT now()
);

-- site_metrics
CREATE TABLE IF NOT EXISTS site_metrics (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    site_id UUID NOT NULL REFERENCES sites(id),
    recorded_date DATE NOT NULL,
    canopy_cover_pct FLOAT,
    ndvi FLOAT,
    carbon_tco2e FLOAT,
    biodiversity_index FLOAT
);

-- alembic version tracking
CREATE TABLE IF NOT EXISTS alembic_version (
    version_num VARCHAR(32) NOT NULL PRIMARY KEY
);

INSERT INTO alembic_version (version_num)
VALUES ('0001_initial_schema')
ON CONFLICT (version_num) DO NOTHING;
"""


async def run():
    ssl_ctx = ssl.create_default_context()
    print(f"Connecting to: {RAW_URL.split('@')[1]}")  # host only, no password
    conn = await asyncpg.connect(RAW_URL, ssl=ssl_ctx)
    try:
        print("Connected. Running migration...")
        await conn.execute(MIGRATION_SQL)
        tables = await conn.fetch(
            "SELECT tablename FROM pg_tables WHERE schemaname='public' ORDER BY tablename"
        )
        print("\n✅ Migration complete. Tables in public schema:")
        for row in tables:
            print(f"  - {row['tablename']}")
    finally:
        await conn.close()


if __name__ == "__main__":
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(run())
