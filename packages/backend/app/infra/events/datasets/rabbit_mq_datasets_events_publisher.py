from aio_pika.abc import AbstractConnection, AbstractChannel

from app.infra.events.datasets.dataset_events_publisher import DatasetsEventsPublisher
from app.workers.schemas.dataset_processing_event import DatasetProcessingEvent
from app.core.queues import queue_settings
from app.infra.events.base import EventMessage


class RabbitMQDatasetsEventsPublisher(DatasetsEventsPublisher):
    def __init__(
        self,
        connection: AbstractConnection,
        channel: AbstractChannel,
    ):
        super().__init__(
            connection,
            channel,
            exchange_id=queue_settings.DATASET_PROCESSING_EXCHANGE,
            routing_key=queue_settings.DATASET_PROCESSING_ROUTING_KEY,
        )

    async def publish_dataset_processing_event(self, payload: DatasetProcessingEvent) -> None:
        await self.publish(EventMessage(
            event="dataset_processing_event",
            payload=payload,
        ))
