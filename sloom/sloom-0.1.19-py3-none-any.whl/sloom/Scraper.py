from bs4 import BeautifulSoup
from .Topic import *
from .Core.List import *
from .Core.Terminal import *

BS4_SETTING = 'html.parser'

class Scraper:
    """
    Param:
        response: Response
    Attributes:
        title: str
        topic: [Topic]
        date: datetime
        url: str
    """
    def __init__(self, resonpse) -> None:
        self.response = resonpse
        self.title = self.getTitle()
        self.topic = List(Topic)
        self.date = None
        self.url = resonpse.url
        self.origin = self.response.origin
        self._soup = BeautifulSoup(resonpse.text, BS4_SETTING)

    def getTitle(self):
        """
        Get The title of a webpage
        """
        titles = List(str)
        for title in self._soup.find_all("title"):
            return title.text
            
    
    def getTopics(self):
        """
        Get topics of a webpage
        """
        pass
    
    def getDate(self):
        """
        Gets date of webpage
        """
        pass

    
    def clean(self):
        """
        Remove all style and js tags
        """
        # parse html content
    
        for data in self._soup(['style', 'script']):
            # Remove tags
            data.decompose()
    
        # return data by retrieving the tag content
        return ' '.join(self._soup.stripped_strings)

    def __str__(self):
        return f"""
        title = {self.title}
        topic = {self.topic}
        date = {self.date}
        url = {self.url}
        origin = {self.origin}
        """

