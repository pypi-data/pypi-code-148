from typing import List

import numpy as np
import numpy.typing as npt
import pandas as pd


def calculate_iqr(data: npt.ArrayLike) -> np.dtype[np.float64]:
    """ Calculates the IQR (interquartile range) for a given array of values.

    There is already an available library under scipy.stats for this, but this wrapper method around numpy is slightly
    faster.

    Args:
       data (array_like): The values for which the IQR will be computed.

    Returns:
       The IQR of <data> as a np.float64 value.
    """
    q1, q3 = np.percentile(data, [25, 75])  # TODO: Fix for NaN values
    return q3 - q1


def iqr_outlier_detection(data: npt.ArrayLike, threshold_factor: float = 1.5) -> npt.NDArray[np.dtype[np.bool_]]:
    """ Detects outliers using the IQR method.

    Any values further than <threshold_factor> * IQR from the median are detected as outliers.

    Args:
       data (array_like): The values on which we want to apply outlier detection.
       threshold_factor (float): Used to calculate the range beyond which we detect everything as outliers.
         Defaults to 1.5.

   Returns:
      A numpy array of the same dimensionality as <data>, where an element is True if the element with the same index in
      <data> is an outlier or False otherwise.
    """
    q1, q3 = np.percentile(data, [25, 75]) # TODO: Fix for NaN values
    iqr = q3 - q1
    lower_bound = q1 - (threshold_factor * iqr)
    upper_bound = q3 + (threshold_factor * iqr)
    return (data > upper_bound) | (data < lower_bound)


def group_by_aggr(df: pd.DataFrame, by: List[str], aggr_col: str, aggr_func: str):
    """ Groups the dataframe by the columns specified and performs an aggregation.

    If we perform a count, size or sum aggregation, the function also returns an extra column with the percentage
    of the aggregated value with respect to the sum of all aggregated values. E.g. if there are 10 rows and we perform
    a groupby and count, a row with an aggregated count value of 2 will have 20% (2/10).

    Args:
        df: The pandas dataframe with the data.
        by: A list of the columns to group by.
        aggr_col: The column to perform the aggregation on.
        aggr_func: The name of the function which will be used when aggregating.

    Returns:
        A pd.DataFrame with the distinct value combinations of the columns included in the <by> argument,
        as well as their aggregated values and percentage in the input dataframe <df>. The percentage
        column is named 'pct'.
    """
    percentage_col = 'pct'
    groupby_df = df.groupby(by)[aggr_col].aggregate(aggr_func).reset_index(name=aggr_func)\
        .sort_values(by=aggr_func, ascending=False)
    if aggr_func in {'sum', 'count', 'size'}:
        groupby_df[percentage_col] = groupby_df[aggr_func] / groupby_df[aggr_func].sum() * 100.0
    return groupby_df
