import logging
import asyncio

from aio_pika.abc import AbstractChannel
from pydantic import BaseModel

from core.models.outbox.outbox import Outbox
from core.tasks.publisher.outbox_task_publisher import OutboxTaskPublisher
from core.utils.provider import Factory
from core.tasks.base import TaskEnvelope

from workers.common.sleep import IDLE_SLEEP, ACTIVE_SLEEP
from workers.consumers.base import AbstractConsumer


logger = logging.getLogger(__name__)


class OutboxConsumer(AbstractConsumer[Outbox[BaseModel]]):
    def __init__(self, outbox_task_publisher_factory: Factory[OutboxTaskPublisher, AbstractChannel]) -> None:
        super().__init__()
        self._outbox_task_publisher_factory = outbox_task_publisher_factory

    async def __aenter__(self):
        await super().__aenter__()

        self._outbox_task_publisher = self._outbox_task_publisher_factory(
            self._channel)
        return self

    async def consume(self, event: Outbox[BaseModel]):
        logger.info(
            f"Publishing outbox event: {event.id} of type {event.event_type}")

        await self._outbox_task_publisher.publish(
            event=TaskEnvelope[BaseModel].create_unknown(
                id=event.id,
                task_type=event.event_type,
                payload=event.payload,
                deduplication_key=str(event.id)
            )
        )


async def publish_outbox_events():
    shutdown_event = asyncio.Event()

    while not shutdown_event.is_set():
        async with OutboxConsumer(
            outbox_task_publisher_factory=OutboxTaskPublisher
        ) as consumer:
            events = await consumer.outbox.fetch_batch()

            if len(events) == 0:
                await asyncio.sleep(IDLE_SLEEP)
                continue

            for event in events:
                await consumer.consume(event)

            await consumer.outbox.batch_mark_as_published([event.id for event in events])
            await consumer.uow.commit()

            await asyncio.sleep(ACTIVE_SLEEP)
