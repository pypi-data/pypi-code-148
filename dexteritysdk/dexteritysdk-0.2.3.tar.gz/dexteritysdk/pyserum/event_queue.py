from typing import List, Iterable

from dexteritysdk.pyserum.structs.event_queue import EventQueueHeader, Register, Event, FillEvent, OutEvent
from dexteritysdk.pyserum.layouts.event_queue import EVENT_QUEUE_HEADER_LAYOUT, REGISTER, EVENT_NODE_LAYOUT, EventType


class EventQueue:
    _header: EventQueueHeader
    _register: Register
    _events: List[Event]

    def __init__(self, header: EventQueueHeader, register: Register, events: List[Event]):
        self._header = header
        self._register = register
        self._events = events

    def __iter__(self) -> Iterable[Event]:
        return self.items()

    def items(self) -> Iterable[Event]:
        for e in self._events:
            yield e

    @staticmethod
    def from_bytes(buffer: bytes) -> "EventQueue":
        header_size = EVENT_QUEUE_HEADER_LAYOUT.sizeof()
        register_size = REGISTER.sizeof()

        header = EVENT_QUEUE_HEADER_LAYOUT.parse(buffer[:header_size])
        register = REGISTER.parse(buffer[header_size:header_size+register_size])
        events = EventQueue.__build_events(buffer, header_size + register_size, header.head, header.count,
                                           header.event_size)

        return EventQueue(
            EventQueueHeader.from_construct(header),
            Register.from_construct(register),
            events
        )

    @staticmethod
    def __build_events(buffer: bytes, header_offset: int, head: int, count: int, event_size: int) -> List[Event]:
        result = []
        for i in range(count):
            node_offset = header_offset + ((i * event_size + head) % (len(buffer) - header_offset))
            event = EVENT_NODE_LAYOUT.parse(buffer[node_offset:node_offset + event_size])
            if event.tag == EventType.FILL:
                result.append(FillEvent.from_construct(event.data))
            else:
                result.append(OutEvent.from_construct(event.data))
        return result
