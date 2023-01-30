from decimal import Decimal
from ..models.orderbook import Orderbook, OrderbookEntry


def price_volume(x: OrderbookEntry):
    return Decimal(x[0]), Decimal(x[1])


def get_price_from_tuple(x: OrderbookEntry) -> Decimal:
    return Decimal(x[0])


def get_volume_from_tuple(x: OrderbookEntry) -> Decimal:
    return Decimal(x[1])


def get_bids(x: Orderbook) -> list[OrderbookEntry]:
    return x["bids"]


def get_asks(x: Orderbook) -> list[OrderbookEntry]:
    return x["asks"]


def top_bid_price(x: Orderbook) -> Decimal:
    return get_price_from_tuple(get_bids(x)[0])


def lowest_ask_price(x: Orderbook) -> Decimal:
    return get_price_from_tuple(get_asks(x)[0])
