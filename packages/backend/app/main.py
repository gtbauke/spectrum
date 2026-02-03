from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.api.v1.routes.datasets import datasets_router
from app.api.v1.routes.models import models_router
from app.infra.events.rabbitmq import rabbitmq_manager


@asynccontextmanager
async def lifespan(app: FastAPI):
    await rabbitmq_manager.connect()
    yield
    await rabbitmq_manager.close()

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

app.include_router(
    prefix="/api/v1/models",
    router=models_router
)
