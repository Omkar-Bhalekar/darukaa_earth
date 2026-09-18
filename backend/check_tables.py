import asyncio
import os
import ssl
import sys

import asyncpg
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))

RAW_URL = os.environ["DATABASE_URL"].replace("postgresql+asyncpg://", "postgresql://")


async def check():
    conn = await asyncpg.connect(RAW_URL, ssl=ssl.create_default_context())
    tables = await conn.fetch(
        "SELECT tablename FROM pg_tables WHERE schemaname='public' ORDER BY tablename"
    )
    ver = await conn.fetch("SELECT version_num FROM alembic_version")
    print("Tables:", [r["tablename"] for r in tables])
    print("Alembic version:", [r["version_num"] for r in ver])
    await conn.close()


if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
asyncio.run(check())
