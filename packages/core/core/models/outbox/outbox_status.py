from enum import StrEnum


class OutboxStatus(StrEnum):
    """The status of event that occurred in the outbox."""

    PENDING = "pending"
    PROCESSED = "processed"
    FAILED = "failed"
