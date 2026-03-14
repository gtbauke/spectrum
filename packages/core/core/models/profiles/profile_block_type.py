from enum import StrEnum


class ProfileBlockType(StrEnum):
    INFERENCE = "inference"
    MARKDOWN = "markdown"
    METADATA = "metadata"
    DATASETS = "datasets"
    JOBS = "jobs"

    def is_system_block(self) -> bool:
        return self in [ProfileBlockType.DATASETS, ProfileBlockType.JOBS, ProfileBlockType.METADATA]
