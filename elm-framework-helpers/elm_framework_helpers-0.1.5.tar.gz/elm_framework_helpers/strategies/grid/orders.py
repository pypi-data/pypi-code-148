from dataclasses import dataclass
from decimal import Decimal
import decimal

from logging import getLogger

logger = getLogger(__name__)

def compute_grid_prices( * ,
    price_decimal_places: int,
    center_price: Decimal,
    gap: Decimal,
    order_count: int,
) -> list[Decimal]:
    with decimal.localcontext() as context:
        context.rounding = decimal.ROUND_DOWN
        initial_price = round(center_price - gap, price_decimal_places)
    prices = []
    for i in range(order_count):
        is_even = bool(i % 2)
        multiplier = (-1 * (i // 2)) if is_even else (2 + i // 2)
        prices.append(initial_price + gap * multiplier)
    return prices


__all__ = [
    "compute_grid_prices"
]