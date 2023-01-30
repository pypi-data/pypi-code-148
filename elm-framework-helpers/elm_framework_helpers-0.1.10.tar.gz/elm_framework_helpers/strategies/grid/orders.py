from decimal import Decimal
import decimal

from logging import getLogger

logger = getLogger(__name__)

from typing import NamedTuple

class GridPrices(NamedTuple):
    initial: Decimal
    grid: list[Decimal]

def get_initial_price(center_price: Decimal, price_decimal_places: int) -> Decimal:
    with decimal.localcontext() as context:
        context.rounding = decimal.ROUND_DOWN
        return round(center_price, price_decimal_places)

def compute_grid_prices( * ,
    price_decimal_places: int,
    center_price: Decimal,
    gap: Decimal,
    order_count: int,
) -> GridPrices:
    initial_price = get_initial_price(center_price, price_decimal_places)
    return compute_grid_prices_skewed(
        price_decimal_places = price_decimal_places,
        center_price = center_price,
        low_price = initial_price - (Decimal(order_count / 2)) * gap,
        gap = gap,
        order_count = order_count,
    )


def compute_grid_prices_skewed(* ,
    price_decimal_places: int,
    center_price: Decimal,
    low_price: Decimal,
    gap: Decimal,
    order_count: int,
) -> GridPrices:
    initial_price = get_initial_price(center_price, price_decimal_places)
    buy_prices = []
    for i in range(order_count):
        price = initial_price - gap * (i+1)
        if price < low_price:
            break
        buy_prices.append(price)
    sell_prices_count = order_count - len(buy_prices)
    prices = []
    for i in range(sell_prices_count):
        if buy_prices:
            prices.append(buy_prices.pop(0))
        prices.append(
            initial_price + gap * (i+1)
        )
    if buy_prices:
        prices += buy_prices
    return GridPrices(initial_price, prices)


__all__ = [
    "compute_grid_prices",
    "compute_grid_prices_skewed",
    "get_initial_price",
    "GridPrices",
]