from .. import RGBColour, HexColour

def rgb_to_hex(rgb: RGBColour) -> HexColour:
    """Converts :class:`RGBColour` to :class:`HexColour`

    Parameters
    ------------
    rgb: :class:`RGBColour`
        The RGB value to convert.
    """
    hex_string = int("".join([hex(x).lstrip("0x") for x in list(rgb.value)]), 16)

    return HexColour(value = hex_string)