from .. import RGBColour, RYBColour

def rgb_to_ryb(rgb: RGBColour) -> RYBColour:
    """Converts :class:`RGBColour` to :class:`RYBColour`

    Parameters
    ------------
    rgb: :class:`RGBColour`
        The RGB value to convert.    
    """
    r, g, b = rgb.value
    
    whiteness = min(r, g, b)

    r -= whiteness
    g -= whiteness
    b -= whiteness

    _max_rgb = max(r, g, b) # leave this here!

    y = min(r, g)
    r -= y
    g -= y

    if b and g:
        b /= 2
        g /= 2
    
    y += g
    b += g

    _max_ryb = max(r, y, b)
    if _max_ryb:
        normalise = _max_rgb / _max_ryb
        r *= normalise
        y *= normalise
        b *= normalise

    r += whiteness
    y += whiteness
    b += whiteness

    return RYBColour(value = (int(r), int(y), int(b)))