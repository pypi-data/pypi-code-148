def tighten_scatter_plot(ax, lim=None, identity=True, **line_kwargs):
    """Tightens scatter plot so that limits on both axes are equal, and
    equalizes aspect ratio.

    Parameters
    ----------
    ax : matplolib.axis
        Axis object.
    lim : list
        The limits of the scatter plot.
    identity : bool
        If True, an identity line is plotted.
    line_kwargs : kwargs
        A dictionary of keyword arguments for the identity line.

    Returns
    -------
    ax : matplotlib.axis
        Axis object, now tightened.
    """
    # Set limits if not provided
    if lim is None:
        lim = ax.get_xlim()
    elif lim == 'x':
        lim = ax.get_xlim()
    elif lim == 'y':
        lim = ax.get_ylim()
    # Equalize limits and aspect ratio
    ax.set_xlim(lim)
    ax.set_ylim(lim)
    ax.set_aspect('equal')
    # Plot identity line if requested
    if identity:
        ax.plot(lim, lim, **line_kwargs)
    return ax
