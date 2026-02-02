import aio_pika

from app.core.config import settings


class RabbitMQManager:
    def __init__(self):
        self._connection: aio_pika.abc.AbstractRobustConnection | None = None
        self._channel: aio_pika.abc.AbstractChannel | None = None

    async def connect(self) -> None:
        if self._connection:
            return

        self._connection = await aio_pika.connect_robust(
            host=settings.RABBITMQ_HOST,
            port=settings.RABBITMQ_PORT,
            login=settings.RABBITMQ_USER,
            password=settings.RABBITMQ_PASSWORD,
        )

        self._channel = await self._connection.channel()

    async def close(self) -> None:
        if self._connection:
            await self._connection.close()
            self._connection = None
            self._channel = None

    @property
    def connection(self) -> aio_pika.abc.AbstractRobustConnection:
        if not self._connection:
            raise RuntimeError("RabbitMQ connection is not established.")

        return self._connection

    @property
    def channel(self) -> aio_pika.abc.AbstractChannel:
        if not self._channel:
            raise RuntimeError("RabbitMQ channel is not established.")

        return self._channel


rabbitmq_manager = RabbitMQManager()
