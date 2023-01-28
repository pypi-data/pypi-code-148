import pandas as pd
from pysentimentanalyzer.get_aggregated_sentiment_score import aggregate_sentiment_score

def convert_to_likert(df, col):
    """Convert the sentiment scores to a likert scale from 1-5
    
    Parameters
    ----------
    df : Pandas DataFrame
        DataFrame containing the text to perform sentiment analysis
    col : string
        Name of the column of text in the Dataframe

    Returns
    -------
    string:
        description of the likert scale value
    int:
        likert scale value
        
    Examples
    --------
    >>> convert_to_likert(counts)
    """
    if not isinstance(df, pd.DataFrame):
        raise Exception("The first parameter should be a Pandas DataFrame.")
    if not (col in list(df.columns)):
        raise Exception("The column parameter should be a column in the DataFrame.")
    agg_score = aggregate_sentiment_score(df, col)
    if agg_score >= -1 and agg_score < -0.6:
        return "very negative", 1
    elif agg_score >= -0.6 and agg_score < -0.2:
        return "negative", 2
    elif agg_score >= -0.2 and agg_score <= 0.2:
        return "neutral", 3
    elif agg_score > 0.2 and agg_score <= 0.6:
        return "positive", 4
    elif agg_score >0.6 and agg_score <= 1:
        return "very positive", 5
    else:
        raise Exception("Aggregate compound score not in the valid range.")
    