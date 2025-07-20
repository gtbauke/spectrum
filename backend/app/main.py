from fastapi import FastAPI
from app.resources.datasets.routes import dataset_router
from app.versioning import APIVersionMiddleware
from contextlib import asynccontextmanager
from app.resources.services.services import get_all_services


@asynccontextmanager
async def lifespan(app: FastAPI):
    all_services = await get_all_services()
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

app.add_middleware(APIVersionMiddleware)
app.include_router(dataset_router, prefix="/api/v1",
                   tags=["v1", "datasets"])
