import matplotlib.pyplot as plt
import numpy as np

from .axes import append_marginal_axis


def scale_values_to_cmap(values, cmap):
    """Gets the RGBA color values on a colormap for values in an array, scaled
    to the minimum and maximum values in the array.

    Parameters
    ----------
    values : np.ndarray
        The values that must be scaled to the colormap.
    cmap : string
        The matplotlib colormap to use.

    Returns
    -------
    colors : np.ndarray, shape (n_values, 4)
        The RGBA color values corresponding to each value, spanning the entire
        color map.
    """
    min_val = np.min(values)
    max_val = np.max(values)
    scaled_values = (values - min_val) / max_val
    colors = plt.get_cmap(cmap)((255 * scaled_values).astype('int'))
    return colors


def append_colorbar_to_axis(
    ax, mappable, spacing=0.05, width=0.05, which='x', **kwargs
):
    """Appends a colorbar to a provided axis, such that the colobar matches the
    dimensions of the axis.

    Can either be appended vertically (extending the x-axis) or horizontally
    (extending the y-axis).

    Parameters
    ----------
    ax : matplotlib object
        An axis object for which to add a colorbar.
    mappable : matplotlib object
        A mappable object for the colobar.
    spacing : float
        The spacing, as a fraction of axis width or height, between the colorbar
        axis and the axis.
    width : float
        The width of the colorbar, as a fraction of the axis width or height.
    which : string
        Either 'x' or 'y', denoting whether the colobrbar is vertical or
        horizontal, respectively.

    Returns
    -------
    cb : matplotlib object
        The colorbar.
    cax : matplotlib object
        The colorbar axes.
    """
    # Use helper function to construct colorbar axes
    cax = append_marginal_axis(ax, spacing, width, which)
    # Create colorbar with mappable
    fig = ax.get_figure()
    cb = fig.colorbar(mappable, cax=cax, **kwargs)
    return cb, cax
