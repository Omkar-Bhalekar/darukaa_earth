import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse

from app.config import settings
from app.database import engine
from app.routers import auth, metrics, projects, sites

logger = logging.getLogger("darukaa")
logging.basicConfig(level=logging.INFO)

app = FastAPI(title="Darukaa.Earth API")


class CatchUnhandledErrorsMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            return await call_next(request)
        except Exception:
            logger.exception(
                "Unhandled error on %s %s", request.method, request.url.path
            )
            return JSONResponse(
                {"detail": "Internal server error"}, status_code=500
            )


# Inner middleware first so CORS can still attach headers on 500s.
app.add_middleware(CatchUnhandledErrorsMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_origin_regex=r"https://.*\.onrender\.com",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(projects.router)
app.include_router(sites.router)
app.include_router(metrics.router)


@app.get("/")
async def root():
    return {"status": "ok", "app": "Darukaa.Earth API"}


@app.get("/health")
async def health():
    async with engine.connect() as conn:
        await conn.execute(text("SELECT 1"))
    return {"status": "ok"}
