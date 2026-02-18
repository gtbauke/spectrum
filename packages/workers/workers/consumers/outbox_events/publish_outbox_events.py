import logging
import asyncio

from workers.common.sleep import IDLE_SLEEP, ACTIVE_SLEEP
from workers.common.get_uow import get_uow
from workers.infra.rabbitmq.setup import setup_all
from workers.infra.rabbitmq.session import create_connection


logger = logging.getLogger(__name__)

# TODO: I copied the OutboxORM model from the backend package, we should
# consider moving it to the core package to avoid duplication and ensure consistency


async def publish_outbox_events():
    connection, channel = await create_connection()
    await setup_all(channel)

    shutdown_event = asyncio.Event()

    while not shutdown_event.is_set():
        async with get_uow() as uow:
            events = await uow.outbox.fetch_batch()

            if len(events) == 0:
                await asyncio.sleep(IDLE_SLEEP)
                continue

            for event in events:
                # TODO: publish event to message broker
                logger.info(f"Publishing event {event.id} to message broker")

            await uow.commit()
            await asyncio.sleep(ACTIVE_SLEEP)

    await channel.close()
    await connection.close()
