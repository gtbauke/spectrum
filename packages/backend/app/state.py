import aio_pika

from app.core.adapters.events.aio_pika_broker import AioPikaBroker


class AppState:
    rabbitmq_connection: aio_pika.abc.AbstractRobustConnection | None = None
    message_broker: AioPikaBroker | None = None


state = AppState()
