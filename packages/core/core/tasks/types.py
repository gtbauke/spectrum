from enum import StrEnum


class TaskType(StrEnum):
    DATASET_PROCESSING = "dataset.process"
    MODEL_TRAINING = "model.train"
