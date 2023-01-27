import matplotlib.pyplot as plt


def get_default_ccycle():
    """Returns the default color cycle as a list of hexcodes."""
    return plt.rcParams['axes.prop_cycle'].by_key()['color']


def hex_to_rgb(color, alpha=None):
    """Converts a color written as a hex code into RGB values (or RGBA, if
    desired).

    Parameters
    ----------
    color : string
        The color, as a hex code.
    alpha : float or None
        If float, the alpha value is added onto the RGB list. Otherwise, no
        alpha value is added.

    Returns
    -------
    rgb : list of floats
        The RGB values.
    """
    # Remove hex hash which is sometimes placed in by default
    if color[0] == '#':
        color = color[1:]

    as_bytes = list(bytes.fromhex(color))
    rgb = [b / 255 for b in as_bytes]
    # Include alpha if provided
    if alpha is not None:
        rgb = rgb + [alpha]
    return rgb
