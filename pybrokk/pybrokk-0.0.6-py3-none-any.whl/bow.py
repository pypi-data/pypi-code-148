import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer

def bow(df):
    """
    Converts the last column of the data frame to a bag of words and return it 
    along with other columns of the data frame.
    
    Parameters
    ----------
    df : data frame
        a data frame with the last column of raw text

           
    Returns
    ----------
    df_bow : data frame
        a data frame which consists of the n-1 first columns of the input data frame as its n-1 first columns,
        plus a bag of words of the input data frame in its following numerous columns. 

        
    Examples
    ----------
    >>> df = pd.DataFrame({
  "url": ["https://www.cnn.com/world",
          "https://www.foxnews.com/world",
          "https://www.cbc.ca/news/world"],
  "url_id": ["cnn1","foxnews1","cbc1"],
  "text": ["Instagram has a faster chance of reaching me than CNN, and if I really want to know what's going on, I refresh my Twitter feed.",
           "I would appear on Fox News more easily than I would NPR.",
           "CBC has a very important mandate to bind Canada together in both official languages, tell local stories, and make sure we have a sense of our strength, our culture, our stories."]
})

    >>> df_bow(df)
            ===============================  ==========  ============================== 
                        url                    url_id             text                   
            ===============================  ==========  ============================== 
             https://www.cnn.com/world         cnn1       Instagram has a faster ...       
             https://www.foxnews.com/world     foxnew1    I would appear on Fox ...        
             https://www.cbc.ca/news/world     cbc1       CBC has a very important ...     
                
                
            ======== ====== ========     ====== ========= ======
             appear   bind   canada  ...  tell	 twitter   want
            ======== ====== ========     ====== ========= ======
               0        0       0    ...   0       1        1
               1        0       0    ...   0       0        0
               0        1       1    ...   1       0        0
    """
    words = CountVectorizer()
    words_matrix = words.fit_transform(df.iloc[:,-1])
    words_array = words_matrix.toarray()
    df_temp = pd.DataFrame(data=words_array, columns = words.get_feature_names_out())
    df_temp = df_temp.set_index(df.index)
    df_bow = pd.concat([df ,df_temp], axis=1)
    return df_bow
