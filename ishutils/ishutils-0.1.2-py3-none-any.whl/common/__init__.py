from enum import StrEnum

__all__: list[str] = ["ActionType", "Status"]


class ActionType(StrEnum):
    COPY = "COPY"
    DOWNLOAD = "DOWNLOAD"
    EXTRACT = "EXTRACT"
    MOVE = "MOVE"
    REMOVE = "REMOVE"
    RUN = "RUN"


class Status(StrEnum):
    FAILURE = "FAILURE"
    RUNNING = "RUNNING"
    SKIPPED = "SKIPPED"
    SUCCESS = "SUCCESS"
