from __future__ import annotations

from typing import Iterable, List, Union

from dexteritysdk.pyserum.layouts.slab import SlabType
from dexteritysdk.pyserum.serum_types import OrderInfo, Order

from dexteritysdk.pyserum.enums import Side
from dexteritysdk.pyserum.structs.slab import Slab, SlabInnerNode, SlabLeafNode
from dexteritysdk.codegen.dex.types import Fractional


class OrderBook:
    """Represents an order book."""

    _is_bids: bool
    _slab: Slab
    _price_offset: Fractional
    _tick_size: Fractional

    def __init__(self, slab: Slab, decimals: int, price_offset: Fractional, tick_size: Fractional) -> None:
        self._is_bids = (slab._header.tag == SlabType.BIDS)
        self._slab = slab
        self._decimals = decimals
        self._price_offset = price_offset
        self._tick_size = tick_size

    @staticmethod
    def get_price_from_key(key: int, tick_size: Fractional, price_offset: Fractional) -> float:
        return ((key >> 96) * tick_size - price_offset).value

    @staticmethod
    def key_is_bid(key: int) -> bool:
        return (key >> 63) & 1 != 0

    def __get_price_from_slab(self, node: Union[SlabInnerNode, SlabLeafNode]) -> float:
        """Get price from a slab node key.

        The key is constructed as the (price << 64) + (seq_no if ask_order else !seq_no).
        """
        return OrderBook.get_price_from_key(node.key, self._tick_size, self._price_offset)

    @staticmethod
    def from_bytes(buffer: bytes, decimals: int, price_offset: Fractional, tick_size: Fractional) -> OrderBook:
        """Decode the given buffer into an order book."""
        slab = Slab.from_bytes(buffer[:])
        return OrderBook(slab, decimals, price_offset, tick_size)

    def get_l2(self, depth: int) -> List[OrderInfo]:
        """Get the Level 2 market information."""
        descending = self._is_bids
        # The first element of the inner list is price, the second is quantity.
        levels: List[List[float]] = []
        for node in self._slab.items(descending):
            price = self.__get_price_from_slab(node)
            if len(levels) > 0 and levels[len(levels) - 1][0] == price:
                levels[len(levels) - 1][1] += node.quantity
            elif len(levels) == depth:
                break
            else:
                levels.append([price, node.quantity])
        return [
            OrderInfo(
                price=price_lots,
                size=size_lots / (10 ** self._decimals),
            )
            for price_lots, size_lots in levels
        ]

    def __iter__(self) -> Iterable[Order]:
        return self.orders()

    def orders(self) -> Iterable[Order]:
        for node in self._slab.items():
            price = self.__get_price_from_slab(node)

            yield Order(
                order_id=node.key,
                client_id=node.client_order_id,
                info=OrderInfo(
                    price=price,
                    size=node.quantity / (10 ** self._decimals),
                ),
                side=Side.BUY if self._is_bids else Side.SELL,
            )
