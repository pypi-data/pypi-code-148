from typing  import Tuple

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from python_accelerate.data_science.utils import group_by_aggr
from python_accelerate.visualize import clean_up_plot


def pretty_aggr_barplot(df: pd.DataFrame, by_col: str, aggr_func: str, aggr_col: str, title: str, top_rows: int = 15,
                        fig_size_inches: Tuple[int] = (5, 5), horizontal: bool = True, aggr_metric: str = None,
                        **kwargs):
    """ Computes and visualizes in a barplot the frequencies of the values in the <count_column> column.

    The barplot includes only as many values as it's specified through the <top_rows> argument. The plotted values and
    their frequencies are also ordered from the highest to the lowest frequency.

    Args:
        df: The dataframe with the data to visualize.
        by_col: The column based on which we will group by rows and aggregate their values for the <aggr_col> column.
        aggr_func: The function to use for aggregation (e.g. 'sum' or 'size').
        aggr_col: The column which we will perform aggregation on.
        title: The title of the plot.
        top_rows: The number of distinct values to include in the plot.
        horizontal: If set to True, the barplot is horizontal.
        aggr_metric: The metric of the column that we aggregate. That is only used for visualization purposes. If this
            is '$' then a dollar will appear next to the visualized aggregated values.
        fig_size_inches: A tuple with the size of the plot in terms of the x and y axes, in inches.
        kwargs: Extra keyword arguments that can be passed to visualize.clean_up_plot before plotting the barplot.
    """
    groupby_df = group_by_aggr(df=df, by=[by_col], aggr_col=aggr_col, aggr_func=aggr_func)[:top_rows]

    # Create bar labels that denote the percentage and occurrence count.
    if aggr_func in {'sum', 'count', 'size'}:
        data_tuples = list(groupby_df[[aggr_func, 'pct']].itertuples(index=False, name=None))
        bar_labels = [f"{t[1]:.2f}% ({t[0]:.0f}{aggr_metric if aggr_metric else ''})" for t in data_tuples]
    else:
        data_tuples = list(groupby_df[[aggr_func]].itertuples(index=False, name=None))
        bar_labels = [f"{t[0]:.0f}{aggr_metric if aggr_metric else ''}" for t in data_tuples]

    orient = 'h' if horizontal else 'v'
    x_col_name = aggr_func if horizontal else by_col
    y_col_name = by_col if horizontal else aggr_func

    ax = sns.barplot(data=groupby_df, x=x_col_name, y=y_col_name, palette='dark:#5A9_r',
                     orient=orient, edgecolor="0", linewidth=0.35)
    ax.set_title(title, fontsize=18, y=1.05)
    ax.bar_label(ax.containers[0], labels=bar_labels, label_type='edge', padding=4.0)

    ax.figure.set_size_inches(*fig_size_inches)
    clean_up_plot(ax, **kwargs)
    plt.show()


