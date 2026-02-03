import json

from aio_pika import Message
from pydantic import BaseModel

from app.infra.events.models.model_events_publisher import ModelEventsPublisher
from app.workers.schemas.start_model_training_event import StartModelTrainingEvent
from app.core.queues import queue_settings


class RabbitMQModelEventsPublisher(ModelEventsPublisher):
    async def publish(self, event: str, payload: BaseModel) -> None:
        message = Message(
            body=json.dumps({
                "event": event,
                "payload": payload.model_dump(mode="json"),
            }).encode("utf-8")
        )

        exchange = await self._channel.get_exchange(queue_settings.MODEL_TRAINING_EXCHANGE)
        await exchange.publish(
            message,
            routing_key=queue_settings.MODEL_TRAINING_ROUTING_KEY,
        )

    async def publish_start_training_event(
        self,
        payload: StartModelTrainingEvent
    ) -> None:
        await self.publish("start_model_training_event", payload)
