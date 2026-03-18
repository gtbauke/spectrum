from enum import StrEnum


class JobRunType(StrEnum):
    QUEUED = "queued"
    WAITING = "waiting"
    RUNNING = "running"
    SUCCESSFUL = "successful"
    FAILED = "failed"
    KILLED = "killed"
    DELETED = "deleted"
