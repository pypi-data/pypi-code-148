from _decimal import Decimal
from typing import Union


class Money:

    def __init__(self, amount: Union[Decimal, str, int], currency: str) -> None:
        self.amount: Decimal = Decimal(amount)
        self.currency: str = str(currency)

    def __add__(self, other) -> Decimal:
        if self.currency != other.currency:
            raise Exception('')

        return self.amount + other.amount
