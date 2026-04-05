import asyncio
import logging

import aio_pika

from core.common.config import Settings
from core.common.logging import setup_logging
from core.utils.broker_constants import MAIN_EXCHANGE_NAME

from adapters.consumer import AioPikaConsumer
from adapters.noop_broker import NoopMessageBroker
from handlers.run_created import RunCreatedHandler
from handlers.inference_run_requested import InferenceRunRequestedHandler

logger = logging.getLogger(__name__)

WORKER_QUEUE_NAME = "workers.training"
INFERENCE_QUEUE_NAME = "workers.inference"


async def main() -> None:
    setup_logging()

    settings = Settings()

    logger.info("Connecting to RabbitMQ at %s...", settings.RABBITMQ_URL)

    connection = await aio_pika.connect_robust(
        settings.RABBITMQ_URL,
    )

    async with connection:
        channel = await connection.channel()
        await channel.set_qos(prefetch_count=1)

        noop_broker = NoopMessageBroker()

        run_created_handler = RunCreatedHandler(
            broker=noop_broker,
        )

        inference_handler = InferenceRunRequestedHandler(
            broker=noop_broker,
        )

        training_consumer = AioPikaConsumer(
            channel=channel,
            exchange_name=MAIN_EXCHANGE_NAME,
            queue_name=WORKER_QUEUE_NAME,
            handlers=[run_created_handler],
        )

        inference_consumer = AioPikaConsumer(
            channel=channel,
            exchange_name=MAIN_EXCHANGE_NAME,
            queue_name=INFERENCE_QUEUE_NAME,
            handlers=[inference_handler],
        )

        await asyncio.gather(
            training_consumer.start(),
            inference_consumer.start()
        )

        logger.info("Worker is running. Press Ctrl+C to exit.")

        try:
            await asyncio.Future()
        except asyncio.CancelledError:
            logger.info("Worker shutting down...")


if __name__ == "__main__":
    asyncio.run(main())
