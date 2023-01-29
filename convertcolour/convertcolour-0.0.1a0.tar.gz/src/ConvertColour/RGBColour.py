class RGBColour:
    """Represents an RGB colour object.
    
    .. versionadded:: 1.0
    
    Attributes
    ------------
    value: :class:`tuple[int, int, int]`
        The RGB values of the colour.
    r: :class:`int`
        The R (red) value of the colour.
    g: :class:`int`
        The G (green) value of the colour.
    b: :class:`int`
        The B (blue) value of the colour.

    Methods
    ---------
    `str(RGBColour) -> str:`
        Returns the colour formatted as "`rgb(255, 171, 59)`".
    `repr(RGBColour) -> str:`
        Returns the colour formatted as "`<RGBColour r=255, g=171, b=59>`".
    """

    __slots__ = (
        "value",
        "r",
        "g",
        "b"
    )

    def __init__(self, value: tuple[int, int, int] = None, r: int = 0, g: int = 0, b: int = 0):
        if value is not None:
            self.value = value
        else:
            self.value = (r, g, b)

        self.r, self.g, self.b = value

    def __str__(self):
        return f"rgb{self.value}"

    def __repr__(self):
        return f"<RGBColour r={self.r} g={self.g} b={self.b}>"