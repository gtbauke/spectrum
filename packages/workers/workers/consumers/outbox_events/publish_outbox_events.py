import logging
import asyncio

from pydantic import BaseModel

from core.models.outbox.outbox import Outbox

from workers.common.sleep import IDLE_SLEEP, ACTIVE_SLEEP
from workers.consumers.base import AbstractConsumer


logger = logging.getLogger(__name__)


class OutboxConsumer(AbstractConsumer[Outbox[BaseModel]]):
    async def consume(self, event: Outbox[BaseModel]):
        logger.info(f"Consuming outbox event {event.id}")


async def publish_outbox_events():
    shutdown_event = asyncio.Event()

    while not shutdown_event.is_set():
        async with OutboxConsumer() as consumer:
            events = await consumer.outbox.fetch_batch()

            if len(events) == 0:
                await asyncio.sleep(IDLE_SLEEP)
                continue

            for event in events:
                await consumer.consume(event)

            await asyncio.sleep(ACTIVE_SLEEP)
