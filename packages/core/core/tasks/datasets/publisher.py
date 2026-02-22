from core.tasks.base import TaskEnvelope
from core.tasks.datasets.task import DatasetProcessTaskPayload
from core.tasks.datasets.success import DatasetProcessingSuccessEvent
from core.tasks.datasets.failure import DatasetProcessingFailureEvent
from core.tasks.publisher.base import AbstractTaskPublisher


class DatasetTaskPublisher(AbstractTaskPublisher):
    async def publish_process_request(self, task: TaskEnvelope[DatasetProcessTaskPayload]) -> None:
        await self.publish(task)

    async def publish_success(self, event: TaskEnvelope[DatasetProcessingSuccessEvent]) -> None:
        await self.publish(event)

    async def publish_failure(self, event: TaskEnvelope[DatasetProcessingFailureEvent]):
        await self.publish(event)
