import numpy as np
import string
import warnings


from .style import check_latex_style_on


def _bold_text(text):
    """Bold text helper function."""
    return '\n'.join(['\\textbf{' + line + '}' for line in text.split('\n')])


def _strip_text(text):
    """Strip text helper function."""
    return text.replace('_', ' ')


def fix_labels_for_tex_style(text):
    """Fixes a string or list of strings for usage in LaTeX style.

    Parameters
    ----------
    text : str or list
        The text, as a single string, or list of strings.

    Returns
    -------
    fixed : str or list
        The fixed text.
    """
    if isinstance(text, str):
        fixed = _strip_text(text)
    elif isinstance(text, list):
        fixed = [_strip_text(s) for s in text]
    else:
        raise ValueError('Text must be a string or list of strings.')
    return fixed


def bold_text(text):
    """Bolds a string or list of strings in LaTeX fashion.

    This function converts the strings to raw strings.

    Parameters
    ----------
    text : str or list
        The text, as a single string, or list of strings.

    Returns
    -------
    bolded : str or list
        The bolded text.
    """
    if not check_latex_style_on():
        warnings.warn("LaTeX style is not turned on. " +
                      "Use use_latex_style() to turn LaTeX style on before bolding text.",
                      RuntimeWarning)
        return text

    if isinstance(text, str):
        bolded = _bold_text(text)
    elif isinstance(text, list) or isinstance(text, np.ndarray):
        bolded = [_bold_text(s) for s in text]
    else:
        raise ValueError('Text must be a string or list of strings.')
    return bolded


def bold_axis_ticklabels(ax, which='both'):
    """Bolds axis ticklabels.
    
    Parameters
    ----------
    ax : matplotlib.axis.Axis
        The matplotlib axis for which to apply bolding.
    which : string
        The axis to which to bold ticklabels: 'x', 'y', or 'both'.

    Returns
    -------
    ax : list
        The axis, with tick labels now bolded.
    """
    if which == 'x' or which == 'both':
        ticklabels = ax.get_xticklabels()
        for ii, label in enumerate(ticklabels):
            text = label.get_text()
            label.set_text(bold_text(text))
            ticklabels[ii] = label
        ax.set_xticklabels(ticklabels)

    if which == 'y' or which == 'both':
        ticklabels = ax.get_yticklabels()
        for ii, label in enumerate(ticklabels):
            text = label.get_text()
            label.set_text(bold_text(text))
            ticklabels[ii] = label
        ax.set_yticklabels(ticklabels)
    return ax


def apply_subplot_labels(
    axes, labels=None, case='lower', bold=False, x=-0.15, y=1.05, ha='center',
    va='center', size=15, **kwargs
):
    """Applies labels to subplots.

    Parameters
    ----------
    axes : matplotlib.axis.Axis, or list
        The matplotlib axes for which to apply labels.
    labels : list of str, default None
        The subplot labels. If None, an alphabetical list will be used.
    case : str
        The case of the subplot labels. Only used if labels is not provided.
        Options are 'lower' and 'upper'.
    bold : bool
        If True, bolds the labels in LaTeX fashion.
    x : float
        The x-offset of the label, in axis space.
    y : float
        The y-offset of the label, in axis space.
    ha, va : str
        The horizontal and vertical alignments.
    size : int
        The size of the label.

    Returns
    -------
    axes : list
        The subplot axes, now labeled.
    """
    if not isinstance(axes, (list, np.ndarray)):
        axes = [axes]
    elif isinstance(axes, np.ndarray) and axes.ndim > 1:
        axes = axes.ravel()
    n_axes = len(axes)

    # Create and bold labels, if necessary
    if labels is None:
        if case == 'lower':
            labels = list(string.ascii_lowercase)[:n_axes]
        elif case == 'upper':
            labels = list(string.ascii_uppercase)[:n_axes]
    if bold:
        labels = bold_text(labels)
    # Apply label to each axis
    for label, ax in zip(labels, axes):
        ax.text(x=x,
                y=y,
                s=label,
                ha=ha,
                va=va,
                size=size,
                transform=ax.transAxes,
                **kwargs)
    return axes


def add_significance_label(
    ax, bounds, label=None, which='top', spacing=0.01, width=0.05,
    color='black', lw=1, fontsize=20
):
    """Adds a significance label to a plot, with optional annotation.

    Parameters
    ----------
    ax : matplotlib.axis.Axis
        The matplotlib axis for which to add the significance marker.
    bounds : tuple, list, or np.ndarray
        The bounds for the significance marker, either on the x- or y-axis.
    label : string, default None
        The annotation label for the significance marker. If None, no label
        is added.
    which : string
        Either 'top', 'bottom', 'left', or 'right', indicating which spine
        the significance marker is added to.
    spacing : float
        The spacing between the significance marker and axis, in axis
        coordinates.
    width : float
        The width of the signifiance marker "stubs".
    color : string
        The color of the signifiance marker.
    lw : float
        The linewidth of the significance marker.
    fontsize : int
        The size of the label.

    Returns
    -------
    ax : list
        The axis, now labeled.
    """
    min_bound = np.min(bounds)
    max_bound = np.max(bounds)

    if which == "top" or which == "bottom":
        min_stub = 1 + spacing
        max_stub = 1 + spacing + width
    elif which == "left" or which == "right":
        min_stub = -spacing
        max_stub = -spacing - width

    if which == 'top' or which == "bottom":
        stub1_x = [min_bound, min_bound]
        stub1_y = [min_stub, max_stub]
        stub2_x = [max_bound, max_bound]
        stub2_y = [min_stub, max_stub]
        spine_x = [min_bound, max_bound]
        spine_y = [max_stub, max_stub]
        trans = ax.get_xaxis_transform()
    elif which == "right" or which == "left":
        stub1_x = [min_stub, max_stub]
        stub1_y = [max_bound, max_bound]
        stub2_x = [min_stub, max_stub]
        stub2_y = [min_bound, min_bound]
        spine_x = [max_stub, max_stub]
        spine_y = [min_bound, max_bound]
        trans = ax.get_yaxis_transform()

    # First stub
    ax.plot(
        stub1_x,
        stub1_y,
        color=color,
        lw=lw,
        transform=trans,
        clip_on=False)
    # Second stub
    ax.plot(
        stub2_x,
        stub2_y,
        color=color,
        lw=lw,
        transform=trans,
        clip_on=False)
    # Spine
    ax.plot(
        spine_x,
        spine_y,
        color=color,
        lw=lw,
        transform=trans,
        clip_on=False)
    if label is not None:
        ax.text(
            x=np.mean(bounds),
            y=max_stub,
            s=label,
            transform=trans,
            ha='center',
            va='bottom',
            fontsize=fontsize,
            clip_on=False)
    return ax
