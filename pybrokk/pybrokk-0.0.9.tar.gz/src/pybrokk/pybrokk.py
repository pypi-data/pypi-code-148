import requests
from bs4 import BeautifulSoup
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer

def create_id(urls):
    """
    Convert a list of provided urls into a list of unique identifiers for use in downstream functions
    
    Parameters
    ----------
    urls: list
        A list of urls as strings
        
    Returns
    ----------
    ids: list
        A list of unique identifiers as strings
        
    Examples
    ----------
    >>> from pybrokk.create_id import create_id
    >>> create_id(['https://www.reddit.com/r/nba/', 'https://www.reddit.com/r/nfl/', 'https://vancouver.craigslist.org/search/apa', 'https://www.kijiji.ca/b-real-estate/richmond-bc/c34l1700288'])
    ['reddit1', 'reddit2', 'craigslist1', 'kijiji1']
    """
    ids = []
    ids_dict = {}
    for url in urls:
        website_split = url.split(".")
        website_name = website_split[1]
        if website_name in ids_dict:
            ids_dict[website_name]["count"] += 1
        else:
            ids_dict[website_name] = {"count": 1}
        ids.append(website_name + str(ids_dict[website_name]["count"]))
        
    return ids

def text_from_url(urls):
    """
    This function takes a list of URLs and returns the parsed text as scraped from the URL using Beautiful Soup

    Parameters
    ----------
        urls: list
            List of URLs to scrape as strings
    
    Returns
    -------
    texts: dictionary
        Dictionary containing the url as keys and parsed text output as values

    Examples
    --------
    >>> text_from_url(["https://realpython.github.io/fake-jobs/jobs/senior-python-developer-0.html", "https://realpython.github.io/fake-jobs/jobs/energy-engineer-1.html"])
    >>> {'https://realpython.github.io/fake-jobs/jobs/senior-python-developer-0.html': '\n\n\n\n\nFake Python\n\n\n\n\n\n\n        Fake Python\n      \n\n        Fake Jobs for Your Web Scraping Journey\n      \n\n\n\n\nSenior Python Developer\nPayne, Roberts and Davis\n\nProfessional asset web application environmentally friendly detail-oriented asset. Coordinate educational dashboard agile employ growth opportunity. Company programs CSS explore role. Html educational grit web application. Oversea SCRUM talented support. Web Application fast-growing communities inclusive programs job CSS. Css discussions growth opportunity explore open-minded oversee. Css Python environmentally friendly collaborate inclusive role. Django no experience oversee dashboard environmentally friendly willing to learn programs. Programs open-minded programs asset.\nLocation: Stewartbury, AA\nPosted: 2021-04-08\n\n\n\n\n\n\n\n',
        'https://realpython.github.io/fake-jobs/jobs/energy-engineer-1.html': '\n\n\n\n\nFake Python\n\n\n\n\n\n\n        Fake Python\n      \n\n        Fake Jobs for Your Web Scraping Journey\n      \n\n\n\n\nEnergy engineer\nVasquez-Davidson\n\nParty prevent live. Quickly candidate change although. Together type music hospital. Every speech support time operation wear often.\nLocation: Christopherville, AA\nPosted: 2021-04-08\n\n\n\n\n\n\n\n'}

    
    """
    parse_res = {}

    for url in urls:
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")
        parse_res.update({url:soup.text})
    return parse_res

def duster(urls):
    """
    Prepares a pandas dataframe by webscraping raw text from a list of urls ready to be input into a machine learning model.
    
    Parameters
    ----------
    urls: list
        list of target urls as strings

    Returns
    ----------
    df: pandas dataframe
        A dataframe with the webpage identifiers as a index, the raw url, and the raw text from the webpage with extra line breaks removed.
        
    Examples
    ----------
    >>> from pybrokk.duster import duster
    >>> duster(['https://www.cnn.com/world', 'https://www.foxnews.com/world', 'https://www.cbc.ca/news/world'])
                                        url                                           raw_text
    id
    cnn1          https://www.cnn.com/world   World news - breaking news, video, headlines ...
    foxnews1  https://www.foxnews.com/world  World | Fox NewsFox News   U.S.PoliticsMediaOp...
    cbc1      https://www.cbc.ca/news/world  World - CBC NewsContentSkip to Main ContentAcc...         
    """
    #scrape text from the web
    output = text_from_url(urls)

    #create Dataframe from dictionary output of text_from_url()
    df = pd.DataFrame.from_dict(output, orient='index', columns=["raw_text"]).reset_index().rename(columns={"index":"url"})
    
    #remove line breaks
    df['raw_text'] = df['raw_text'].str.replace("\n", "")
    
    #add id as index
    df['id'] = create_id(df['url'].tolist())
    df = df.set_index('id')
    
    return df

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



