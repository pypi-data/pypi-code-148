from .. import RYBColour, RGBColour

def rgb_to_ryb(ryb: RYBColour) -> RGBColour:
    """Converts :class:`RYBColour` to :class:`RGBColour`

    Parameters
    ------------
    ryb: :class:`RYBColour`
        The RYB value to convert.    
    """
    r, y, b = ryb.value

    whiteness = min(r, y, b)

    r -= whiteness
    y -= whiteness
    b -= whiteness

    _max_ryb = max(r, y, b) # leave this here!

    g = min(y, b)
    y -= g
    b -= g

    if b and g:
        b *= 2
        g *= 2

    r += y
    g += y

    _max_rgb = max(r, g, b)
    if _max_ryb:
        normalise = _max_ryb / _max_rgb
        r *= normalise
        g *= normalise
        b *= normalise

    r += whiteness
    g += whiteness
    b += whiteness

    return RYBColour(value = (int(r), int(g), int(b)))