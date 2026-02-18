from core.tasks.success import AbstractTaskSuccessEvent


class DatasetProcessingSuccessEvent(AbstractTaskSuccessEvent):
    """Event emitted when a dataset has been successfully processed."""
