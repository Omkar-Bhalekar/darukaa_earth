from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.routers import auth, metrics, projects, sites

app = FastAPI(title="Darukaa.Earth API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL],
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
