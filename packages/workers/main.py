import asyncio
import logging
import os
import platform
import sys

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

from db.common.session import AsyncSessionLocal

from services.heartbeat import HeartbeatService
from services.control import ControlListener

logger = logging.getLogger(__name__)

WORKER_QUEUE_NAME = "workers.training"
VALIDATION_QUEUE_NAME = "workers.validation"
INFERENCE_QUEUE_NAME = "workers.inference"


def _build_worker_id(worker_type: str) -> str:
    """Generate a deterministic, human-readable worker identifier."""
    hostname = platform.node()
    pid = os.getpid()
    return f"{worker_type}-{hostname}-{pid}"


async def _run_worker_loop(
    *,
    settings: Settings,
    connection,
    worker_type: str,
    worker_id: str,
) -> bool:
    """Run the consumer loop once.

    Returns ``True`` if the loop was terminated by a restart command
    (and should be re-entered), ``False`` otherwise.
    """
    channel = await connection.channel()
    await channel.set_qos(prefetch_count=1)

    exchange = await channel.declare_exchange(
        name=MAIN_EXCHANGE_NAME,
        type=aio_pika.ExchangeType.TOPIC,
        durable=True,
    )

    broker = AioPikaBroker(exchange)

    # -- Heartbeat service -----------------------------------------------------
    heartbeat = HeartbeatService(
        worker_id=worker_id,
        worker_type=worker_type,
        session_factory=AsyncSessionLocal,
        interval_seconds=settings.WORKER_HEARTBEAT_INTERVAL_SECONDS,
    )
    heartbeat.start()

    # -- Control listener ------------------------------------------------------
    control = ControlListener(channel=channel, worker_id=worker_id)
    await control.start()

    # -- Event handlers --------------------------------------------------------
    run_created_handler = RunCreatedHandler(
        broker=broker,
        heartbeat=heartbeat,
    )

    run_finished_handler = RunFinishedHandler(
        broker=broker,
        heartbeat=heartbeat,
    )

    inference_handler = InferenceRunRequestedHandler(
        broker=broker,
        heartbeat=heartbeat,
    )

    # -- Consumers -------------------------------------------------------------
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
        logger.error(
            "No consumers matched WORKER_TYPE='%s'. Exiting.", worker_type)
        await heartbeat.stop()
        return False

    await asyncio.gather(*tasks)

    logger.info("Worker '%s' is running. Press Ctrl+C to exit.", worker_id)

    # Wait until restart is requested or the process is cancelled
    restart_event = control.get_restart_event()

    try:
        await restart_event.wait()
        logger.warning(
            "Restart event received — exiting process to trigger container restart...")
        await heartbeat.stop()
        await channel.close()
        sys.exit(0)
    except asyncio.CancelledError:
        logger.info("Worker cancelled — shutting down...")
        await heartbeat.stop()
        return False


async def main() -> None:
    setup_logging()

    settings = Settings()
    worker_type = os.getenv("WORKER_TYPE", "all").lower()
    worker_id = _build_worker_id(worker_type)

    logger.info(
        "Starting worker: id=%s, type=%s",
        worker_id, worker_type,
    )
    logger.info("Connecting to RabbitMQ at %s...", settings.RABBITMQ_URL)

    connection = await aio_pika.connect_robust(
        settings.RABBITMQ_URL,
    )

    async with connection:
        try:
            await _run_worker_loop(
                settings=settings,
                connection=connection,
                worker_type=worker_type,
                worker_id=worker_id,
            )
        except asyncio.CancelledError:
            logger.info("Worker shutting down...")
        except Exception:
            logger.exception("Worker loop crashed — restarting in 5s...")
            await asyncio.sleep(5)
            sys.exit(1)

    logger.info("Worker '%s' has exited.", worker_id)


if __name__ == "__main__":
    asyncio.run(main())
