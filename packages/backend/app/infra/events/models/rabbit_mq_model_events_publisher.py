from aio_pika.abc import AbstractConnection, AbstractChannel

from app.infra.events.models.model_events_publisher import ModelEventsPublisher
from app.workers.schemas.start_model_training_event import StartModelTrainingEvent
from app.core.queues import queue_settings
from app.infra.events.base import EventMessage


class RabbitMQModelEventsPublisher(ModelEventsPublisher):
    def __init__(
        self,
        connection: AbstractConnection,
        channel: AbstractChannel,
    ):
        super().__init__(
            connection,
            channel,
            exchange_id=queue_settings.MODEL_TRAINING_EXCHANGE,
            routing_key=queue_settings.MODEL_TRAINING_ROUTING_KEY,
        )

    async def publish_start_training_event(
        self,
        payload: StartModelTrainingEvent,
    ) -> None:
        await self.publish(EventMessage(
            event="start_model_training_event",
            payload=payload,
        ))
