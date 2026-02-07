from fastapi import APIRouter

from app.api.v1.routes.datasets import datasets_router
from app.api.v1.routes.models import models_router
from app.api.v1.routes.inference import inference_router

v1_router = APIRouter(prefix="/api/v1")

v1_router.include_router(
    prefix="/datasets",
    router=datasets_router
)

v1_router.include_router(
    prefix="/models",
    router=models_router
)

v1_router.include_router(
    prefix="/inference",
    router=inference_router
)
