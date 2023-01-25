"""
Provides the emitter type:
* A `Listenable` can listen for events and call the `listen`ing handlers when they occur.
One can be created with the `listenable` function.
* An `Emittable` has the capabilities of a `Listenable` and can `emit` events.
This (as above) invokes all the listening handlers (calls all the functions)
with the `Event` that was just emitted as an argument.
"""

from asyncio import Future
from dataclasses import dataclass
from typing import Callable, Generic, Optional, TypeVar


Event = TypeVar("Event")


@dataclass(frozen=True, slots=True)
class Listenable(Generic[Event]):
    """
    An interface that allows many different places of code
    to listen for events (invoking a callback) from a source
    """

    listen: Callable[[Callable[[Event], None]], Callable[[], None]]


@dataclass(frozen=True, slots=True)
class Emittable(Listenable, Generic[Event]):
    """
    An extension to the `Listenable` interface that can emit events to it
    """

    emit: Callable[[Event], None]


def emittable(
    start: Optional[Callable[[Callable[[Event], None]], Callable[[], None]]] = None,
) -> Emittable[Event]:
    """Creates an `Emittable` emitter that allows both emitting events and listening for events"""

    listeners: set[Callable[[Event], None]] = set()

    stop: Callable[[], None]

    def listen(handler: Callable[[Event], None]) -> Callable[[], None]:
        nonlocal stop
        if start is not None and len(listeners) == 0:
            stop = start(emit)

        listeners.add(handler)

        def unlisten():
            listeners.remove(handler)
            if start is not None and len(listeners) == 0:
                stop()

        return unlisten

    def emit(event: Event):
        for handler in listeners.copy():
            handler(event)

    return Emittable(listen=listen, emit=emit)


def listenable(
    start: Optional[Callable[[Callable[[Event], None]], Callable[[], None]]] = None,
) -> Listenable[Event]:
    """
    Creates a `Listenable` emitter that allows listening for events

    The optional `start` argument is a function that receives
    an `emit` argument and returns a `stop` function.
    `start` is called when the number of listeners to the emitter goes from 0 to 1,
    and `stop` is called when the number of listeners goes from 1 to 0.
    This behavior can be used to emit events only when
    there is any interest in them (there is at least one handler `listen`ing for them).
    """

    emitter = emittable(start)
    return Listenable(listen=emitter.listen)


def successor(emitter: Listenable[Event]) -> Future[Event]:
    """
    Returns a `Future` that can be `await`ed to get the next event
    once it's been emitted by the `emitter`
    """

    future = Future()

    def handler(event: Event):
        unlisten()
        future.set_result(event)

    unlisten = emitter.listen(handler)
    return future


MappedEvent = TypeVar("MappedEvent")


def mapped(
    emitter: Listenable[Event],
    fn: Callable[[Event], MappedEvent],  # pylint: disable=invalid-name
) -> Listenable[MappedEvent]:
    """
    Calls `fn` on every event emitted by `emitter` and emits the result to a new `Listenable`
    """

    def start(emit):
        def handler(event: Event):
            emit(fn(event))

        unlisten = emitter.listen(handler)
        return unlisten

    return listenable(start)
