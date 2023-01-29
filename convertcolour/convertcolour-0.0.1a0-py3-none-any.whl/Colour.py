import HexColour, RGBColour, RYBColour
from .converters import rgb_to_hex, rgb_to_ryb, hex_to_rgb, ryb_to_rgb

__all__ = (
    "Colour"
)

class Colour:
    """Represents a colour object.

    .. versionadded:: 1.0

    Attributes
    ------------
    hex: :class:`HexColour`
        The hex value of the colour.
    rgb: :class:`RGBColour`
        The RGB value of the colour.
    ryb: :class:`RYBColour`
        The RYB value of the colour.
    """

    __slots__ = (
        "hex",
        "rgb",
        "ryb"
    )

    def __init__(self, hex = None, rgb = None, ryb = None):
        self.hex: HexColour
        self.rgb: RGBColour
        self.ryb: RYBColour

        if hex is not None:
            self.hex = HexColour(hex)
            self.rgb = hex_to_rgb(self.hex)
            self.ryb = rgb_to_ryb(self.rgb)
        elif rgb is not None:
            self.rgb = RGBColour(rgb)
            self.hex = rgb_to_hex(self.rgb)
            self.ryb = rgb_to_ryb(self.rgb)
        elif ryb is not None:
            self.ryb = RYBColour(ryb)
            self.rgb = ryb_to_rgb(self.ryb)
            self.hex = rgb_to_hex(self.rgb)