class HexColour:
    """Represents a hex colour object.

    .. versionadded:: 1.0

    Attributes
    ------------
    value: :class:`str`
        The hex value of the colour.

    Methods
    ---------
    `str(HexColour) -> str:`
        Returns the colour formatted as "`#FFAB3B`".
    `repr(HexColour) -> str:`
        Returns the colour formatted as "`<HexColour value=0xffab3b>`".
    `int(HexColour) -> int:`
        Returns the colour formatted as "`16755515`".
    `hex(HexColour) -> int:`
        Returns the colour formatted as "`0xffab3b`".
    """

    __slots__ =(
        "value",
        "_raw_value"
    )

    def __init__(self, value: int = 0) -> None:
        self.value = hex(value)
        self._raw_value = value

    def __str__(self):
        hex_value: str = self.value.lstrip('0x')
        return f"#{'0' * (6 - len(hex_value))}{hex_value}".capitalize()

    def __repr__(self):
        return f"<HexColour value={self.value}>"

    def __int__(self):
        return int(self._raw_value)
    
    def __index__(self):
        return int(self.value, 16)