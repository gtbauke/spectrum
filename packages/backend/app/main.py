from fastapi import FastAPI

from app.api.v1.routes.datasets import datasets_router

app = FastAPI()

app.include_router(
    prefix="/api/v1/datasets",
    router=datasets_router
)
