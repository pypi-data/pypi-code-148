from dataclasses import dataclass


@dataclass
class Message:
    """A message is a task instantiation that is published to or read from the broker."""

    id: str
    name: str
    args: tuple
    kwargs: dict
    queue: str
