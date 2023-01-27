def append_marginal_axis(ax, spacing=0.05, width=0.05, which='x'):
    """Appends a marginal plot to a provided axis.

    Parameters
    ----------
    ax : matplotlib object
        An axis object for which to add a colorbar axis.
    spacing : float
        The spacing, as a fraction of axis width or height, between the marginal
        axis and the provided axis.
    width : float
        The width of the axis, as a fraction of the axis width or height.
    which : string
        Either 'x' or 'y', denoting whether the colobrbar is vertical or
        horizontal, respectively.

    Returns
    -------
    cax : matplotlib object
        The colorbar axes.
    """
    # Get axis dimensions and figure
    [[x0, y0], [x1, y1]] = ax.get_position().get_points()

    # Add colorbar axes
    fig = ax.get_figure()
    if which == 'x':
        marginal = fig.add_axes(
            [x1 + spacing * (x1 - x0),
             y0,
             width * (x1 - x0),
             y1 - y0])
    elif which == 'y':
        marginal = fig.add_axes(
            [x0,
             y1 + spacing * (y1 - y0),
             x1 - x0,
             width * (y1 - y0)])
    else:
        raise ValueError('Must specify whether colorbar extends x or y axis.')
    return marginal
