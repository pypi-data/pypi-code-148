import nltk
import pandas as pd
from nltk.sentiment.vader import SentimentIntensityAnalyzer

nltk.download("vader_lexicon")
nltk.download("punkt")

def get_compound_score(text):
    """
    Calculates a compound sentiment score from text

    Parameters:
    -----------
    text: str
        Input text data as string
    
    Returns:
    --------
    A numeric sentiment score of the text : (float)
    """
    sid = SentimentIntensityAnalyzer()
    score = sid.polarity_scores(text)
    return score["compound"]

def get_sentiment(text):
    """
    Evaluates the type of sentiment from a given text

    Parameters:
    -----------
    text: str
        Input text data as string
    
    Returns:
    --------
    The type of sentiment (positive, negetive or neutral) as a string : (str)
    """
    score = get_compound_score(text)
    if score > 0:
        return "positive"
    if score < 0:
        return "negative"
    return "neutral"

def get_sentiment_and_score(df, col):
    """
    Calculates a compound sentiment score from text

    Parameters:
    -----------
    df: pd.DataFrame
        A DataFrame
    col: 
        The column name of the text column on which sentiment analysis is done
    
    Returns:
    --------
    A Pandas DataFrame with numeric sentiment and its corresponding sentiment type 
    added to the DataFrame : (pd.DataFrame)
    """
    df = df.assign(compound_score=df[col].apply(get_compound_score))
    df = df.assign(sentiment=df[col].apply(get_sentiment))
    return df
