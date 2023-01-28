import requests
from bs4 import BeautifulSoup

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
        

        
        