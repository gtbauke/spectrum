from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.api.v1.router import v1_router
from app.infra.events.rabbitmq import rabbitmq_manager
from app.api.middlewares.correlation_id_middleware import CorrelationIdMiddleware
from app.core.logging import setup_logging
from app.domain.rebuild import rebuild_models


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

app.add_middleware(CorrelationIdMiddleware)
app.include_router(v1_router)
