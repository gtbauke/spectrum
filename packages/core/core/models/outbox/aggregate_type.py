from enum import StrEnum


class AggregateType(StrEnum):
    """
    The AggregateType enum represents the type of an aggregate in the Outbox pattern.
    It is used to categorize messages in the outbox based on the type of aggregate they are associated with.
    """

    DATASET = "dataset"
    MODEL = "model"
