import aio_pika
from aio_pika.abc import AbstractChannel

from app.core.config import settings
from app.core.queues import queue_settings
from app.workers.consumers.dataset_processor_consumer import handle_dataset_processing_message


async def setup_dataset_processing(channel: aio_pika.abc.AbstractChannel):
    datasets_processing_exchange = await channel.declare_exchange(
        name=queue_settings.DATASET_PROCESSING_EXCHANGE,
        type=aio_pika.ExchangeType.DIRECT,
        durable=True,
    )

    datasets_processing_queue = await channel.declare_queue(
        name=queue_settings.DATASET_PROCESSING_QUEUE,
        durable=True,
        arguments={
            "x-dead-letter-exchange": queue_settings.DATASET_PROCESSING_EXCHANGE,
            "x-dead-letter-routing-key": queue_settings.DATASET_PROCESSING_RETRY_ROUTING_KEY,
        }
    )

    datasets_retry_queue = await channel.declare_queue(
        name=queue_settings.DATASET_PROCESSING_RETRY_QUEUE,
        durable=True,
        arguments={
            "x-message-ttl": 30_000,
            "x-dead-letter-exchange": queue_settings.DATASET_PROCESSING_EXCHANGE,
            "x-dead-letter-routing-key": queue_settings.DATASET_PROCESSING_ROUTING_KEY,
        }
    )

    datasets_dlq = await channel.declare_queue(
        name=queue_settings.DATASET_PROCESSING_DEAD_LETTER_QUEUE,
        durable=True,
    )

    await datasets_processing_queue.bind(
        exchange=datasets_processing_exchange,
        routing_key=queue_settings.DATASET_PROCESSING_ROUTING_KEY,
    )

    await datasets_retry_queue.bind(
        exchange=datasets_processing_exchange,
        routing_key=queue_settings.DATASET_PROCESSING_RETRY_ROUTING_KEY,
    )

    await datasets_dlq.bind(
        exchange=datasets_processing_exchange,
        routing_key=queue_settings.DATASET_PROCESSING_DEAD_LETTER_ROUTING_KEY,
    )

    async with datasets_processing_queue.iterator() as dataset_processing_queue_iterator:
        async for message in dataset_processing_queue_iterator:
            await handle_dataset_processing_message(message)

    return channel


async def setup_queues() -> AbstractChannel:
    connection = await aio_pika.connect_robust(
        host=settings.RABBITMQ_HOST,
        port=settings.RABBITMQ_PORT,
        login=settings.RABBITMQ_USER,
        password=settings.RABBITMQ_PASSWORD,
    )

    async with connection:
        channel = await connection.channel()

        await setup_dataset_processing(channel)

    return channel
