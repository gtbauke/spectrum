import aio_pika

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.common.logging import setup_logging
from core.utils.broker_constants import MAIN_EXCHANGE_NAME

from .api.v1 import api_router
from .adapters.events.aio_pika_broker import AioPikaBroker
from .utils.rebuild import *
from .core.config import settings


class AppState:
    rabbitmq_connection: aio_pika.abc.AbstractRobustConnection | None = None
    message_broker: AioPikaBroker | None = None


state = AppState()


@asynccontextmanager
async def lifespan(app: FastAPI):
    state.rabbitmq_connection = await aio_pika.connect_robust(
        settings.RABBITMQ_URL,
    )

    channel = await state.rabbitmq_connection.channel()
    exchange = await channel.declare_exchange(
        name=MAIN_EXCHANGE_NAME,
        type=aio_pika.ExchangeType.TOPIC,
        durable=True,
    )

    state.message_broker = AioPikaBroker(exchange=exchange)
    yield

    if state.rabbitmq_connection:
        await state.rabbitmq_connection.close()

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
        "http://localhost:5173",
        # TODO: add production URL here
    ],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

app.include_router(prefix="/api", router=api_router)
