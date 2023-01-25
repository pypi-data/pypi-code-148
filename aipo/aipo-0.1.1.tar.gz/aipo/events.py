from typing import TYPE_CHECKING, Callable, Dict, List, Tuple

from .utils import ensure_async

if TYPE_CHECKING:
    from .app import AipoApp


class EventManager:
    """Create a new event manager.

    Events are used to trigger actions when certain lifecycle events occur.
    """

    def __init__(self, allowed_events: List[str], app: "AipoApp") -> None:
        self.app = app
        self._receivers: Dict[str, List] = {ev: [] for ev in allowed_events}

    def register(self, event_name: str, receiver: Callable) -> None:
        """Register a receiver for an event.

        Args:
            event_name (str): The name of the event to register the receiver for.
            receiver (Callable): The receiver function to register.
        """
        if event_name not in self._receivers:
            raise KeyError(f"Event {event_name} is not a valid event.")
        self._receivers[event_name].append(receiver)

    async def trigger(self, event_name: str, *args: Tuple, **kwargs: Dict) -> None:
        """Trigger an event.

        Args:
            event_name (str): The name of the event to trigger.
        """
        if event_name not in self._receivers:
            raise KeyError(f"Event {event_name} is not a valid event.")
        for receiver in self._receivers[event_name]:
            await ensure_async(receiver, *args, **kwargs)
