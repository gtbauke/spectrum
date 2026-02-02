from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.api.v1.routes.datasets import datasets_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield

app = FastAPI(
    title="Spectrum Backend",
    description="Backend service for Spectrum application",
    version="1.0.0",
    lifespan=lifespan
)

app.include_router(
    prefix="/api/v1/datasets",
    router=datasets_router
)
