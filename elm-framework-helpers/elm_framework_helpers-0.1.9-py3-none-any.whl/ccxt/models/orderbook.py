from typing import TypedDict, NamedTuple


class OrderbookEntry(NamedTuple):
    price: float
    volume: float


class Orderbook(TypedDict):
    asks: list[OrderbookEntry]
    bids: list[OrderbookEntry]
    symbol: str
    timestamp: int
    datetime: str
    nonce: str
