from abc import ABC
from dataclasses import dataclass

from solana.publickey import PublicKey

from dexteritysdk.pyserum.layouts.event_queue import Side


@dataclass
class EventQueueHeader:
    tag: int
    head: int
    count: int
    event_size: int
    seq_num: int

    @staticmethod
    def from_construct(c_obj):
        return EventQueueHeader(
            c_obj.tag,
            c_obj.head,
            c_obj.count,
            c_obj.event_size,
            c_obj.seq_num
        )


@dataclass
class Register:
    posted_order_id: int
    total_base_quantity: int
    total_quote_quantity: int
    total_base_quantity_posted: int

    @staticmethod
    def from_construct(c_obj):
        if c_obj.register_present:
            return Register(
                c_obj.posted_order_id if c_obj.posted_order_id_present else None,
                c_obj.total_base_qty,
                c_obj.total_quote_qty,
                c_obj.total_base_qty_posted
            )
        return None


@dataclass
class Callback:
    account: PublicKey
    open_orders_idx: int

    @staticmethod
    def from_construct(c_obj):
        return Callback(
            PublicKey(c_obj.account),
            c_obj.open_orders_idx,
        )


class Event(ABC):
    pass


@dataclass
class FillEvent(Event):
    taker_side: Side
    maker_order_id: int
    quote_size: int
    base_size: int
    maker_callback: Callback
    taker_callback: Callback

    @staticmethod
    def from_construct(c_obj):
        return FillEvent(
            c_obj.taker_side,
            c_obj.maker_order_id,
            c_obj.quote_size,
            c_obj.base_size,
            Callback.from_construct(c_obj.maker_callback),
            Callback.from_construct(c_obj.taker_callback),
        )


@dataclass
class OutEvent(Event):
    side: Side
    order_id: int
    base_size: int
    delete: int
    callback: Callback

    @staticmethod
    def from_construct(c_obj):
        return OutEvent(
            c_obj.side,
            c_obj.order_id,
            c_obj.base_size,
            c_obj.delete,
            Callback.from_construct(c_obj.callback),
        )
