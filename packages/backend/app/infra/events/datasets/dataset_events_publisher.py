from abc import abstractmethod

from app.infra.events.base import EventPublisher
from app.workers.schemas.dataset_processing_event import DatasetProcessingEvent


class DatasetsEventsPublisher(EventPublisher):
    @abstractmethod
    async def publish_dataset_processing_event(
        self, payload: DatasetProcessingEvent,
    ) -> None: ...
