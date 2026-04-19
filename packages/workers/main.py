import asyncio
import logging
import os

import aio_pika

from core.common.config import Settings
from core.common.logging import setup_logging
from core.utils.broker_constants import MAIN_EXCHANGE_NAME

from adapters.consumer import AioPikaConsumer
from adapters.noop_broker import NoopMessageBroker
from handlers.run_created import RunCreatedHandler
from handlers.run_finished import RunFinishedHandler
from handlers.inference_run_requested import InferenceRunRequestedHandler
from adapters.aiopika_broker import AioPikaBroker

logger = logging.getLogger(__name__)

WORKER_QUEUE_NAME = "workers.training"
VALIDATION_QUEUE_NAME = "workers.validation"
INFERENCE_QUEUE_NAME = "workers.inference"


async def main() -> None:
    setup_logging()

    settings = Settings()
    worker_type = os.getenv("WORKER_TYPE", "all").lower()

    logger.info("Connecting to RabbitMQ at %s...", settings.RABBITMQ_URL)

    connection = await aio_pika.connect_robust(
        settings.RABBITMQ_URL,
    )

    async with connection:
        channel = await connection.channel()
        await channel.set_qos(prefetch_count=1)

        exchange = await channel.declare_exchange(
            name=MAIN_EXCHANGE_NAME,
            type=aio_pika.ExchangeType.TOPIC,
            durable=True,
        )

        broker = AioPikaBroker(exchange)

        run_created_handler = RunCreatedHandler(
            broker=broker,
        )

        run_finished_handler = RunFinishedHandler(
            broker=broker,
        )

        inference_handler = InferenceRunRequestedHandler(
            broker=broker,
        )

        tasks = []

        if worker_type in ("all", "training"):
            logger.info("Registering training consumer...")
            training_consumer = AioPikaConsumer(
                channel=channel,
                exchange_name=MAIN_EXCHANGE_NAME,
                queue_name=WORKER_QUEUE_NAME,
                handlers=[run_created_handler],
            )
            tasks.append(training_consumer.start())

        if worker_type in ("all", "inference", "iql"):
            logger.info("Registering inference (IQL) consumer...")
            inference_consumer = AioPikaConsumer(
                channel=channel,
                exchange_name=MAIN_EXCHANGE_NAME,
                queue_name=INFERENCE_QUEUE_NAME,
                handlers=[inference_handler],
            )
            tasks.append(inference_consumer.start())

        if worker_type in ("all", "validation", "verification"):
            logger.info("Registering validation (verification) consumer...")
            validation_consumer = AioPikaConsumer(
                channel=channel,
                exchange_name=MAIN_EXCHANGE_NAME,
                queue_name=VALIDATION_QUEUE_NAME,
                handlers=[run_finished_handler],
            )
            tasks.append(validation_consumer.start())

        if not tasks:
            logger.error("No consumers matched WORKER_TYPE='%s'. Exiting.", worker_type)
            return

        await asyncio.gather(*tasks)

        logger.info("Worker is running. Press Ctrl+C to exit.")

        try:
            await asyncio.Future()
        except asyncio.CancelledError:
            logger.info("Worker shutting down...")


if __name__ == "__main__":
    asyncio.run(main())
