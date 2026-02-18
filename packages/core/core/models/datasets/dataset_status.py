from enum import StrEnum


class DatasetStatus(StrEnum):
    PENDING = "PENDING"
    PROCESSING = "PROCESSING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


def can_transition_status(
    current_status: DatasetStatus,
    new_status: DatasetStatus,
) -> bool:
    transitions: dict[DatasetStatus, set[DatasetStatus]] = {
        DatasetStatus.PENDING: {DatasetStatus.PROCESSING, DatasetStatus.FAILED},
        DatasetStatus.PROCESSING: {DatasetStatus.COMPLETED, DatasetStatus.FAILED},
        DatasetStatus.COMPLETED: set(),
        DatasetStatus.FAILED: {DatasetStatus.PENDING},
    }

    return new_status in transitions[current_status]
