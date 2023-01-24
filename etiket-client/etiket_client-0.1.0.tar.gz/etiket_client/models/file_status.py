from enum import Enum


class FileStatus(str, Enum):
    UNAVAILABLE = "unavailable"
    PENDING = "pending"
    AVAILABLE = "available"
    SECURED = "secured"

    def __str__(self) -> str:
        return str(self.value)
