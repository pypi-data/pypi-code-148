# Define here the models for your scraped items
#
# See documentation in:
# <https://docs.scrapy.org/en/latest/topics/items.html>

import sys
from datetime import datetime

import scrapy


class GoldendoodleItem(scrapy.Item):
    """
    **Definition of the output:**
    """
    currentURL = scrapy.Field() 
    """
    currentURL 
        shows the response.url of the actual entry. 
    """
    currentHeaders = scrapy.Field()
    """    
    currentHeaders 
        shows the response.headers of currentURL. 
    """  
    regex_finding = scrapy.Field()
    """  
    finding shows
        the first occurrence of the search string in the whole text of currentURL.
        
        - example: 
            <re.Match object; span=(251, 256), match='latex'> ==> LaTeX
    """  
    regex_findingElements = scrapy.Field()
    """  
    findingElements
        shows the XML elements containing the search string.
    """  
    regex_findingElementsQuery = scrapy.Field()
    """  
    findingElementsQuery
        describes the XPATH to the XML element with the search string.
    """
    webdriver_finding = scrapy.Field()
    webdriver_findingElements = scrapy.Field()
    webdriver_findingElementsQuery = scrapy.Field()
    cleared_webdriver_finding = scrapy.Field()
    cleared_webdriver_findingElements = scrapy.Field()
    cleared_webdriver_findingElementsQuery = scrapy.Field()
