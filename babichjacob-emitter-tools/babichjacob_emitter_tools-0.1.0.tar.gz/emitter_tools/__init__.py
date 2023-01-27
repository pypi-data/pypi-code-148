"Tools for working with emitters"


from asyncio import Queue
from collections import deque
from typing import (
    AsyncGenerator,
    Callable,
    Deque,
    Iterable,
    Optional,
    TypeVar,
    overload,
)

from emitter import Event, Listenable, emittable, listenable, mapped
from option_and_result import E, O, Result
from store import Readable, readable


def events(emitter: Listenable[Event]) -> AsyncGenerator[Event, None]:
    """
    Asynchronously iterate over every event from the `emitter`

    This may be useful if you wish to react to events strictly in order
    of when they were received, waiting for previous work to complete
    before starting to work on the next incoming event.

    # Examples

    Slowly (random speed) print events in order of them being received,
    as a simulation for real work that would take a long and arbitrary amount of time
    in the real world (dealing with I/O).

    >>> from asyncio import gather, sleep
    >>> from random import random

    >>> from emitter import emittable, Emittable

    >>> async def slow_print(event: bytes):
    ...     await sleep(random()*0.1)
    ...     print("I did something for", event)

    >>> my_emitter = emittable()

    >>> # Produce the events
    >>> async def emit_events(emitter: Emittable[bytes]):
    ...     example_bytes = b"abcdefghijkl"
    ...     for byte in iterate_bytes(example_bytes):
    ...         emitter.emit(byte)

    >>> from typing import Iterator
    >>> def iterate_bytes(bytes_: bytes) -> Iterator[bytes]:
    ...     for i in range(len(bytes_)):
    ...         yield bytes_[i:i+1]

    >>> # Consume the events
    >>> async def react_to_events(emitter: Listenable[bytes]):
    ...     async for event in events(emitter):
    ...         await slow_print(event)
    ...
    ...         # Note: This is only here to ensure the function finishes at some point
    ...         # for doctesting purposes
    ...         if event == b"l": break

    >>> # Run both the producer and consumer until they're done
    >>> async def main():
    ...     bytes_emitter = emittable()
    ...     await gather(
    ...         react_to_events(bytes_emitter),
    ...         emit_events(bytes_emitter),
    ...     )

    >>> from asyncio import run
    >>> run(main())
    I did something for b'a'
    I did something for b'b'
    I did something for b'c'
    I did something for b'd'
    I did something for b'e'
    I did something for b'f'
    I did something for b'g'
    I did something for b'h'
    I did something for b'i'
    I did something for b'j'
    I did something for b'k'
    I did something for b'l'
    """

    queue = Queue()

    unlisten = emitter.listen(queue.put_nowait)

    async def generator():
        try:
            while True:
                yield await queue.get()
        finally:
            unlisten()

    return generator()


@overload
def latest(emitter: Listenable[Event], initial_value: Event) -> Readable[Event]:
    ...


@overload
def latest(emitter: Listenable[Event]) -> Readable[Event | None]:
    ...


# I like the way calls to this function behave so I am deliberately ignoring the error
def latest(  # type: ignore
    emitter: Listenable[Event], initial_value: Event = None
) -> Readable[Event | None]:
    """
    Returns a store whose value is the most recent event emitted by the `emitter`,
    or `initial_value`.

    # Examples

    >>> python_releases_emitter = emittable()
    >>> latest_python_version_store = latest(python_releases_emitter)

    >>> unsubscribe = latest_python_version_store.subscribe(
    ...     lambda latest_python_version:
    ...        print("The latest Python release is", latest_python_version)
    ... )
    The latest Python release is None

    >>> python_releases_emitter.emit((2, 7))
    The latest Python release is (2, 7)

    >>> python_releases_emitter.emit((3, 10))
    The latest Python release is (3, 10)

    >>> python_releases_emitter.emit((3, 11))
    The latest Python release is (3, 11)

    >>> # Remember to unsubscribe when done
    >>> unsubscribe()
    """

    return readable(initial_value, emitter.listen)


def filtered(
    emitter: Listenable[Event], predicate: Callable[[Event], bool]
) -> Listenable[Event]:
    """
    Returns an emitter that only emits events from the input `emitter`
    where `predicate(event)` is `True`

    # Examples

    ## Filtering an emitter to even numbers only

    >>> numbers = emittable()
    >>> even_numbers = filtered(numbers, lambda number: number % 2 == 0)
    >>> unlisten = even_numbers.listen(lambda even_number: print("Got an even number", even_number))

    >>> numbers.emit(1)
    >>> numbers.emit(2)
    Got an even number 2
    >>> numbers.emit(3)
    >>> numbers.emit(4)
    Got an even number 4

    >>> unlisten() # Remember to unlisten when done
    """

    def start(emit: Callable[[Event], None]):
        def handler(event: Event):
            if predicate(event):
                emit(event)

        unlisten = emitter.listen(handler)
        return unlisten

    return listenable(start)


Total = TypeVar("Total")


def scan(
    emitter: Listenable[Event], reducer: Callable[[Total, Event], Total], seed: Total
) -> Readable[Total]:
    """
    This is analogous to the `reduce` operation on iterables.

    First, `total` is initialized to `seed`.
    Then, every time an event is emitted, it calls `reducer(total, event)`,
    sets the returned store to the result of this, and assigns `total` to said result
    for the next call (for the next event to be emitted).

    # Examples

    ## Keeping a running total (sum) of emitted numbers

    >>> numbers_emitter = emittable()

    >>> running_total_store = scan(numbers_emitter, lambda total, incoming: total + incoming, 0)

    >>> unsubscribe = running_total_store.subscribe(
    ...     lambda running_total: print("The new total is", running_total)
    ... )
    The new total is 0

    >>> numbers_emitter.emit(7)
    The new total is 7

    >>> numbers_emitter.emit(5)
    The new total is 12

    >>> numbers_emitter.emit(8)
    The new total is 20

    >>> unsubscribe() # Remember to unsubscribe when done


    ## Storing all events emitted

    This is similar to the behavior you can get from using the `recent` function.

    >>> strings_emitter = emittable()

    >>> def add_to_list(strings: list[str], new_entry: str) -> list[str]:
    ...     return [*strings, new_entry]

    >>> all_strings_store = scan(strings_emitter, add_to_list, [])

    >>> unsubscribe = all_strings_store.subscribe(print)
    []

    >>> strings_emitter.emit('hi')
    ['hi']

    >>> strings_emitter.emit('this is')
    ['hi', 'this is']

    >>> strings_emitter.emit('a set of')
    ['hi', 'this is', 'a set of']

    >>> strings_emitter.emit('example strings')
    ['hi', 'this is', 'a set of', 'example strings']

    >>> unsubscribe() # Remember to unsubscribe when done
    """

    def start(set_: Callable[[Total], None]):
        total = seed

        def handler(event: Event):
            nonlocal total

            total = reducer(total, event)
            set_(total)

        unlisten = emitter.listen(handler)
        return unlisten

    return readable(seed, start)


def recent(
    emitter: Listenable[Event], limit: Optional[int] = None
) -> Readable[deque[Event]]:
    """
    Stores up to `limit` (or an unlimited amount if not passed) events emitted by the `emitter`

    Returns a store whose value is a `deque` of those stored events.

    # Examples

    ## Storing an unlimited number of events

    >>> friend_requests_emitter = emittable()

    >>> all_friend_requests_store = recent(friend_requests_emitter)

    >>> unsubscribe = all_friend_requests_store.subscribe(
    ...    lambda all_friend_requests: print(
    ...        "You have pending friend requests from",
    ...        " & ".join(all_friend_requests) + ".",
    ...    )
    ... )
    You have pending friend requests from .

    >>> friend_requests_emitter.emit('Aron')
    You have pending friend requests from Aron.

    >>> friend_requests_emitter.emit('Andrew')
    You have pending friend requests from Aron & Andrew.

    >>> friend_requests_emitter.emit('Alex')
    You have pending friend requests from Aron & Andrew & Alex.

    >>> friend_requests_emitter.emit('Ava')
    You have pending friend requests from Aron & Andrew & Alex & Ava.

    >>> unsubscribe() # Remember to unsubscribe when done
    """

    def reducer(total: Deque[Event], event: Event):
        new = total.copy()
        new.append(event)
        return new

    return scan(emitter, reducer, deque(maxlen=limit))


# TODO: journal, which accompanies each event with a datetime / timestamp

Category = TypeVar("Category")


def categorize(
    emitter: Listenable[Event],
    key: Callable[[Event], Category],
    categories: Iterable[Category],
) -> dict[Category, Listenable[Event]]:
    emits: dict[Category, Callable[[Event], None]] = {}
    listenables: dict[Category, Listenable[Event]] = {}

    active_listeners = 0
    unlisten: Callable[[], None]

    def switch(event: Event):
        destination = key(event)
        if destination not in emits:
            raise KeyError(
                f"{destination!r} is not in {categories!r}, so an event for it cannot be emitted"
            )
        emit = emits[destination]
        emit(event)

    def start_subemitter(i: int):
        def start(_emit: Callable[[Event], None]):
            nonlocal active_listeners

            if not active_listeners:
                nonlocal unlisten
                unlisten = emitter.listen(switch)

            active_listeners |= 1 << i

            def stop():
                nonlocal active_listeners
                active_listeners &= ~(1 << i)

                if not active_listeners:
                    unlisten()

            return stop

        return start

    for i, category in enumerate(categories):
        subemitter = emittable(start_subemitter(i))

        emits[category] = subemitter.emit
        listenables[category] = Listenable(listen=subemitter.listen)

    return listenables


def partitioned(
    emitter: Listenable[Event], predicate: Callable[[Event], bool]
) -> tuple[Listenable[Event], Listenable[Event]]:
    r"""
    Splits an emitter into two emitters:
    * One that emits events from the `emitter` where `predicate(event)` is False
    * One that emits events from the `emitter` where `predicate(event)` is True

    # Examples
    ## Have a separate emitter for integers divisible by 3

    >>> numbers_emitter = emittable()

    >>> numbers_not_divisible_by_3_emitter, numbers_divisible_by_3_emitter = \
    ...     partitioned(numbers_emitter, lambda n: n % 3 == 0)

    >>> unlisten_1 = numbers_not_divisible_by_3_emitter.listen(
    ...    lambda n: print(n, "is not divisible by 3")
    ... )

    >>> unlisten_2 = numbers_divisible_by_3_emitter.listen(
    ...     lambda n: print(n, "is divisible by 3")
    ... )

    >>> numbers_emitter.emit(5)
    5 is not divisible by 3
    >>> numbers_emitter.emit(6)
    6 is divisible by 3
    >>> numbers_emitter.emit(7)
    7 is not divisible by 3
    >>> numbers_emitter.emit(8)
    8 is not divisible by 3
    >>> numbers_emitter.emit(9)
    9 is divisible by 3
    """

    categorized = categorize(emitter, predicate, [False, True])
    return (categorized[False], categorized[True])


def categorize_result(
    emitter: Listenable[Result[O, E]],
) -> tuple[Listenable[O], Listenable[E]]:
    predicate = Result.is_err
    when_ok, when_err = partitioned(emitter, predicate)
    return (mapped(when_ok, Result.unwrap), mapped(when_err, Result.unwrap_err))
