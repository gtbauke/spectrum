from fastapi import FastAPI
from contextlib import asynccontextmanager
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware

from app.versioning import APIVersionMiddleware
from app.services import get_all_services
from app.resources.datasets.routes import dataset_router
from app.resources.jobs.routes import job_router
from app.resources.job_runs.routes import job_runs_router

load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    all_services = get_all_services()
    for service in all_services:
        service.on_server_start()

    yield

    for service in all_services:
        service.on_server_shutdown()

app = FastAPI(
    title="Spectrum API",
    description="API for managing Symbolic Regression datasets",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://localhost:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.add_middleware(APIVersionMiddleware)
app.include_router(dataset_router, prefix="/api/v1",
                   tags=["v1", "datasets"])

app.include_router(job_router, prefix="/api/v1",
                   tags=["v1", "jobs"])

app.include_router(job_runs_router, prefix="/api/v1",
                   tags=["v1", "job_runs"])
