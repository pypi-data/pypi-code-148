from __future__ import annotations
from typing import NamedTuple
from dexteritysdk.pyserum.enums import Side


class OrderInfo(NamedTuple):
    price: float
    """"""
    size: float
    """"""


class Order(NamedTuple):
    order_id: int
    """"""
    client_id: int
    """"""
    info: OrderInfo
    """"""
    side: Side
    """"""
