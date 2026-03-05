from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.common.logging import setup_logging
from .api.v1 import api_router

from app.features.models import *


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield

setup_logging()

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

app.include_router(prefix="/api", router=api_router)
