# imports
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pysentimentanalyzer.helper import *


def sentiment_score_plot(df, col):
    """
    Creates a binned histogram showing count of reviews
    ranging from negative to positive sentiment score.

    Provides the most frequent sentiment score and the corresponding percentage

    Parameters
    ----------
    df : Pandas DataFrame
        DataFrame containing the reviews
    col: String
        Name of the column that contains the reviews

    Returns
    -------
    Plot:
        A plot object

    Examples
    --------
    >>> plot = sentiment_score_plot(df, "column_name")
    >>> plt.show()
    """

    # Check that the first input is dataframe
    if not isinstance(df, pd.DataFrame):
        raise TypeError("The first parameter should be Pandas Dataframe.")

    # Check that the second input is a string
    if not isinstance(col, str):
        raise TypeError("The second parameter should be string dtype")

    # Check that the column exists in dataframe
    if not (col in list(df.columns)):
        raise Exception("The second parameter is not a column in the dataframe")

    # Call the helper function to compute the sentiment and score
    data = get_sentiment_and_score(df, col)

    # Plot the figure
    fig_size = (7, 5)
    f = plt.figure(figsize=fig_size)

    ax = f.add_subplot(1, 1, 1)
    y, x, _ = plt.hist(
        data["compound_score"], density=False, bins=10, label="Sentiment Counts"
    )
    plt.legend(loc="upper right")
    plt.ylabel("Count")
    plt.xlabel("Sentiment Score range")
    plt.title("Distibution of Sentiments")

    # Histogram metrics
    max_counts = y.max()
    min_counts = y.min()
    max_percentage = max_counts / len(data["compound_score"])

    print(
        f"The highest frequency ({max_counts}) of sentiment scores are in range {x[y.argmax()]:.1f} to {x[y.argmax()+1]:.1f} which forms {max_percentage*100:.02f}% of samples in the dataset"
    )

    return f
