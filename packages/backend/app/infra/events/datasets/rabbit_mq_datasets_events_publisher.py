import json

from aio_pika import Message
from pydantic import BaseModel

from app.infra.events.datasets.dataset_events_publisher import DatasetsEventsPublisher
from app.workers.schemas.dataset_processing_event import DatasetProcessingEvent
from app.workers.setup import queue_settings


class RabbitMQDatasetsEventsPublisher(DatasetsEventsPublisher):
    async def publish(self, event: str, payload: BaseModel) -> None:
        message = Message(
            body=json.dumps({
                "event": event,
                "payload": payload.model_dump(mode="json"),
            }).encode("utf-8")
        )

        exchange = await self._channel.get_exchange(queue_settings.DATASET_PROCESSING_EXCHANGE)
        await exchange.publish(
            message,
            routing_key=queue_settings.DATASET_PROCESSING_ROUTING_KEY,
        )

    async def publish_dataset_processing_event(self, payload: DatasetProcessingEvent) -> None:
        await self.publish("dataset_processing_event", payload)
