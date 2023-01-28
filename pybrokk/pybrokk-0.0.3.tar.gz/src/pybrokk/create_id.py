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