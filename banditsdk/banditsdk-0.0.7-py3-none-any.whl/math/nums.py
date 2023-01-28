import math

def round_down(n, decimals=0) -> float:
    """
    This function round down the number.
    It`s custom round (python) + floor(math).
    You can specify a decimals, by second named argument.
    Is not very accurate, because it has a float type.

    :param n: Number to round down
    :type n: int | float
    :param decimals: Amount or numbers after dot/comma
    :type decimals: int
    :return: rounded down number in float type
    """
    decimals = 10**decimals
    return math.floor(n * decimals) / decimals
