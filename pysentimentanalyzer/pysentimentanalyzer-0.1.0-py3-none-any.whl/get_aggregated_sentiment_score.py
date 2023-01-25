import pandas as pd
from pysentimentanalyzer.helper import get_sentiment_and_score

def aggregate_sentiment_score(df, col):
    """
    Returns an aggregated compound score representing sentiment: 
    -1 (most extreme negative) and +1 (most extreme positive). The compound score
    is a normalized score calculated by summing the valence scores of each word in the lexicon.

    Parameters:
    -----------
    df : Pandas DataFrame
        DataFrame containing the reviews
    col : str
        Column name in the dataframe that contains the reviews 

    Returns:
    --------
    aggregated sentiment score of the text rounded to 3 decimal points: (float)
    
    Examples
    --------
    >>> agg_score = aggregate_sentiment(df, "reviews")
    >>> agg_score
    0.81
    """
    if not isinstance(df, pd.DataFrame):
        raise Exception("The first parameter should be a Pandas DataFrame.")
    if not (col in list(df.columns)):
        raise Exception("The column parameter should be a column in the DataFrame.")
    
    sentiment_df = get_sentiment_and_score(df, col)

    agg_compound_score = sentiment_df['compound_score'].mean()

    if not (-1 <= agg_compound_score <= 1):
        raise Exception("Out of bounds error [-1,1], {} is not an aggregated compound score.".format(agg_compound_score))

    if not isinstance(agg_compound_score, float):
        raise Exception("Error in aggregate calculation, {} is not a float value")

    return round(agg_compound_score, 3)
    

    