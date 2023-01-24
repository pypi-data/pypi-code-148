from .cmeel_example import cmeel_add


def cmeel_mult(a: int, b: int) -> int:
    """
    Multiplication by positive integer from our custom addition.

    Super inefficient :)

    >>> cmeel_mult(4, 3)
    12

    >>> cmeel_mult(5, -3)
    0
    """
    ret = 0
    for _ in range(b):
        ret = cmeel_add(ret, a)
    return ret
