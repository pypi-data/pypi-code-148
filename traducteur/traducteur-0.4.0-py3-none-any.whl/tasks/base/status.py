from enum import IntEnum


class TaskStatus(IntEnum):
    NONE = 0
    QUEUED = 1
    RUNNING = 2
    SUCCEEDED = 3
    FAILED = 5