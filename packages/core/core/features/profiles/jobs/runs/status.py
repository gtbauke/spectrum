from enum import StrEnum


class JobRunStatus(StrEnum):
    WAITING = "waiting"
    RUNNING = "running"
    FINISHED = "finished"
    FAILED = "failed"
