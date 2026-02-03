from abc import abstractmethod

from app.infra.events.base import EventPublisher
from app.workers.schemas.start_model_training_event import StartModelTrainingEvent


class ModelEventsPublisher(EventPublisher):
    @abstractmethod
    async def publish_start_training_event(
        self,
        payload: StartModelTrainingEvent
    ) -> None: ...
