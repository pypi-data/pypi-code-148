import matplotlib.pyplot as plt


def clean_up_plot(ax: plt.axes, xlabel: bool = False, ylabel: bool = False,
                  xticklabels: bool = False, yticklabels: bool = False,
                  bottom_ticks: bool = False, left_ticks: bool = False,
                  box_frame=False):
    """ Wrapper around different different matplotlib.pyplot.Axes methods for cleaning up a plot.

    Args:
        ax: The pyplot.Axes object to modify.
        xlabel: If true, the xlabel is deleted.
        ylabel: If true, the ylabel is deleted.
        xticklabels: If true, the x tick labels are deleted.
        yticklabels: If true, the y tick labels are deleted.
        bottom_ticks: If true, the bottom ticks are removed.
        left_ticks: If true, the left ticks are removed.
        box_frame: If true, the box frame around the plot is removed.
    """
    # Clean up plot
    if xlabel:
        ax.set_xlabel('')
    if ylabel:
        ax.set_ylabel('')
    if xticklabels:
        ax.set_xticklabels([])
    if yticklabels:
        ax.set_yticklabels([])
    ax.tick_params(bottom=not bottom_ticks, left=not left_ticks)
    if box_frame:
        ax.set_frame_on(False)
