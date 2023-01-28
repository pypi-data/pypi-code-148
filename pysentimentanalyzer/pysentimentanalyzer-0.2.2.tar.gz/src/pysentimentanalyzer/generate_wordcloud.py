import pandas as pd
from wordcloud import WordCloud
from pysentimentanalyzer.helper import get_sentiment_and_score

def generate_wordcloud(df, col):
    """
    Generate the word cloud of the most common positive and negative words from a given survey in the form of a 
    data frame and create a word cloud.

    Parameters
    ----------
    df : Pandas DataFrame
        DataFrame containing the survey comments
    col : string
        Name of the column of text in the Dataframe

    Returns
    -------
    List:
         A list of three images in the following order: postive, neutral, negative
         A word cloud instance that can be later plotted or saved as an image

    Examples
    --------
     >>> imgs= generate_wordcloud(df, col)
     >>> imgs[0].show() # positive
     >>> imgs[1].show() # negative
     >>> imgs[2].show() # neutral
    """
    if df is None:
        raise TypeError("df must not be None")
    
    if not isinstance(df, pd.DataFrame):
        raise TypeError("df must be a DataFrame")
    
    if col is None:
        raise TypeError("col must not be None") 

    df =  get_sentiment_and_score(df,col) 
    neg_df = df[df["sentiment"] == "negative"]
    pos_df = df[df["sentiment"] == "positive"]
    neutral_df = df[df["sentiment"] == "neutral"]

    negative_messages = " ".join(neg_df[col].tolist())
    positive_messages = " ".join(pos_df[col].tolist())
    neutral_messages = " ".join(neutral_df[col].tolist())


    wordcloud = WordCloud(max_font_size=40, width=800, height=400)
    pos_image = wordcloud.generate(negative_messages).to_image()
    neg_image = wordcloud.generate(positive_messages).to_image()
    neutral_image = wordcloud.generate(neutral_messages).to_image()

    return [pos_image,neutral_image, neg_image]