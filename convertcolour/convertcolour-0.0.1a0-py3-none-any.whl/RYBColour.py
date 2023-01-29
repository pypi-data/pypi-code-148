class RYBColour:
    """Represents an RYB colour object.
    
    .. versionadded:: 1.0
    
    Attributes
    ------------
    value: :class:`tuple[int, int, int]`
        The RYB values of the colour.
    r: :class:`int`
        The R (red) value of the colour.
    y: :class:`int`
        The Y (yellow) value of the colour.
    b: :class:`int`
        The B (vlue) value of the colour.

    Methods
    ---------
    `str(RYBColour) -> str:`
        Returns the colour formatted as "`ryb(206, 255, 59)`".
    `repr(RYBColour) -> str:`
        Returns the colour formatted as "`<RYBColour r=206, y=255, b=59>`".
    """

    __slots__ = (
        "value",
        "r",
        "y",
        "b"
    )

    def __init__(self, value: tuple[int, int, int] = None, r: int = 0, y: int = 0, b: int = 0):
        if value is not None:
            self.value = value
        else:
            self.value = (r, y, b)

        self.r, self.y, self.b = value

    def __str__(self):
        return f"ryb{self.value}"

    def __repr__(self):
        return f"<RYBColour r={self.r} y={self.y} b={self.b}>"