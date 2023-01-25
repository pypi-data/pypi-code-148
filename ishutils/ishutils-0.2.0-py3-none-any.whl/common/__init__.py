from enum import StrEnum

__all__: list[str] = ["ActionType", "Status"]


class ActionType(StrEnum):
    COPY = "COPY"
    DOWNLOAD = "DOWNLOAD"
    EXTRACT = "EXTRACT"
    LINK = "LINK"
    MOVE = "MOVE"
    REMOVE = "REMOVE"
    REPLACE = "REPLACE"
    RUN = "RUN"


class Status(StrEnum):
    FAILURE = "FAILURE"
    RUNNING = "RUNNING"
    SKIPPED = "SKIPPED"
    SUCCESS = "SUCCESS"
