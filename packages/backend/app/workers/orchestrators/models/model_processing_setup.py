import aio_pika
from aio_pika.abc import AbstractChannel

from app.core.config import settings
from app.core.queues import queue_settings
from app.workers.consumers.models.model_processor_consumer import handle_model_training_message


async def setup_model_processing(channel: aio_pika.abc.AbstractChannel):
    exchange = await channel.declare_exchange(
        name=queue_settings.MODEL_TRAINING_EXCHANGE,
        type=aio_pika.ExchangeType.DIRECT,
        durable=True,
    )

    processing_queue = await channel.declare_queue(
        name=queue_settings.MODEL_TRAINING_QUEUE,
        durable=True,
        arguments={
            "x-dead-letter-exchange": queue_settings.MODEL_TRAINING_EXCHANGE,
            "x-dead-letter-routing-key": queue_settings.MODEL_TRAINING_RETRY_ROUTING_KEY,
        }
    )

    retry_queue = await channel.declare_queue(
        name=queue_settings.MODEL_TRAINING_RETRY_QUEUE,
        durable=True,
        arguments={
            "x-message-ttl": 60_000,
            "x-dead-letter-exchange": queue_settings.MODEL_TRAINING_EXCHANGE,
            "x-dead-letter-routing-key": queue_settings.MODEL_TRAINING_ROUTING_KEY,
        }
    )

    dead_letter_queue = await channel.declare_queue(
        name=queue_settings.MODEL_TRAINING_DEAD_LETTER_QUEUE,
        durable=True,
    )

    await processing_queue.bind(
        exchange=exchange,
        routing_key=queue_settings.MODEL_TRAINING_ROUTING_KEY,
    )

    await retry_queue.bind(
        exchange=exchange,
        routing_key=queue_settings.MODEL_TRAINING_RETRY_ROUTING_KEY,
    )

    await dead_letter_queue.bind(
        exchange=exchange,
        routing_key=queue_settings.MODEL_TRAINING_DEAD_LETTER_ROUTING_KEY,
    )

    async with processing_queue.iterator() as processing_queue_iterator:
        async for message in processing_queue_iterator:
            await handle_model_training_message(message)

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

        await setup_model_processing(channel)

    return channel
