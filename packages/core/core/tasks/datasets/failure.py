from core.tasks.failure import AbstractTaskFailureEvent


class DatasetProcessingFailureEvent(AbstractTaskFailureEvent):
    """Event emitted when a dataset processing task fails after all retry attempts."""
    pass
