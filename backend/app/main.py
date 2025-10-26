import time

from contextlib import asynccontextmanager
from app.services.file_service import FileService
from app.tasks.create_sr_model import Boto3SessionOptions
from app.utils.config import Config
from fastapi import FastAPI, Request
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware

from app.versioning import APIVersionMiddleware
from app.resources.datasets.routes import dataset_router
from app.resources.jobs.routes import job_router
from app.resources.job_runs.routes import job_runs_router
from app.logging_config import logger


load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    file_service = FileService(options=Boto3SessionOptions(
        region_name=Config.S3_BUCKET_REGION,
        aws_access_key_id=Config.AWS_ACCESS_KEY,
        aws_secret_access_key=Config.AWS_SECRET_KEY,
    ))

    await file_service.on_server_startup()
    app.state.file_service = file_service

    yield

    await file_service.on_server_shutdown()


app = FastAPI(
    title="Spectrum API",
    description="API for managing Symbolic Regression datasets",
    version="1.0.0",
    lifespan=lifespan
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


@app.middleware("http")
async def log_requests(request: Request, call_next):  # type: ignore
    start = time.time()
    response = await call_next(request)  # type: ignore
    process_time = (time.time() - start) * 1000
    status_code = response.status_code  # type: ignore

    logger.info(
        f"{request.method} {request.url.path} - {status_code} ({process_time:.2f} ms)")

    return response  # type: ignore
