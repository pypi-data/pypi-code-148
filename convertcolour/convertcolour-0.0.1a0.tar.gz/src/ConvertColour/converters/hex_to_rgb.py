from .. import HexColour, RGBColour

def hex_to_rgb(hex: HexColour) -> RGBColour:
    """Converts :class:`HexColour` to :class:`RGBColour`

    Parameters
    ------------
    hex: :class:`HexColour`
        The hex value to convert. 
    """
    hex_string = str(hex).lstrip("#")
    rgb_tuple = tuple([int(x, 16) for x in [(hex_string[i:i+2]) for i in range(0, len(hex_string), 2)]])

    return RGBColour(value = rgb_tuple)