from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.router import v1_router
from app.infra.events.rabbitmq import rabbitmq_manager
from app.utils.rebuild import rebuild_models

from core.common.logging import setup_logging

# TODO: separate UnitOfWork into read and write
# GET endpoints should not use UnitOfWork that has write capabilities
# this will prevent accidental writes and improve API response times

# TODO: try to avoid multiple commands to the database
# see datasets_service.py for example of multiple calls to the database that can be optimized by combining them into a single call
# this will improve performance and reduce the load on the database
# To do this, we need new repository methods


@asynccontextmanager
async def lifespan(app: FastAPI):
    await rabbitmq_manager.connect()
    yield
    await rabbitmq_manager.close()

setup_logging()
rebuild_models()

app = FastAPI(
    title="Spectrum Backend",
    description="Backend service for Spectrum application",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "*"
    ],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(v1_router)
