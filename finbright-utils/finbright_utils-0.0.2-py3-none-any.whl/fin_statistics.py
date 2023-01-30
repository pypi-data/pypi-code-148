import pandas as pd
from statsmodels.tsa.stattools import coint


def correlation(X1: pd.Series, X2: pd.Series) -> int:
    """_summary_

    Args:
        data (pd.DataFrame): A close price dataframe of two coins

    Returns:
        int: correlation coeffiecient between close prices of two coins
    """

    corr_coefficient = X1.corr(X2)

    return corr_coefficient


def cointegration(X1: pd.Series, X2: pd.Series) -> int:
    """_summary_

    Args:
        data (pd.DataFrame): A close price dataframe of two coins

    Returns:
        int: cointegation coeffiecient between close prices of two coins
    """

    score, pvalue, _ = coint(X1, X2)

    return pvalue
