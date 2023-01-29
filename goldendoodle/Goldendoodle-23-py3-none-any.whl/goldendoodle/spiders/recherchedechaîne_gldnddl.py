# -*- coding: utf-8 -*-
"""
This Scrapy Spider searches within a domain vor every occurense of a search string.

Raises:
    none

Yields:
    GoldendoodleItem(scrapy.Item)
"""
import copy
import logging
import os
import sys
# Standard library imports
from datetime import datetime
from gettext import find
# Third party imports
from inspect import currentframe, getframeinfo
from threading import Thread
from time import sleep
from tkinter import UNITS

import regex
import scrapy.utils.log
import tldextract
from lxml import etree
from lxml.html.soupparser import fromstring
from scrapy import Request
from scrapy.linkextractors import IGNORED_EXTENSIONS, LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.utils.log import configure_logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

# Local application imports
import goldendoodle.spiders.items as gi
import goldendoodle.spiders.utils.gldnddl_utils as gu
from goldendoodle.spiders.utils.gldnddl_utils import Gldnddl

logger = logging.getLogger(__name__)

# tbd. extensions which have caused issues
IGNORED_EXTENSIONS += []


class RecherchedechaîneGldddlSpider(CrawlSpider):
    name = 'recherchedechaîne_gldnddl'

    def __init__(self, gldnddlSearchString=None, start_urls=None, option=str(None), *args, **kwargs):
        """Overwrite the Scrapy __init__ function, so that you can pass starting URLs and search String as argument.

        Args:
            gldnddlSearchString (str): default None will cause end.
            start_urls (str): default None will cause end.
            option (str):   None    := default
                            regex   := gldnddlSearchString is a regular expression
                            e-mail  := FUTUREFEATURE; it will enable to search for e-mail addresses
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            calls super().__init__()

        A missing search string will stop the spider with return code 64:

        >>> os.WEXITSTATUS(os.system("scrapy crawl recherchedechaîne_gldnddl -O reports/findings.json -a start_urls='https:to.be,https:or-not-to.be'"))
        64

        Missing start URLs will stop the spider with return code 64:

        >>> os.WEXITSTATUS(os.system("scrapy crawl recherchedechaîne_gldnddl -O reports/findings.json -a gldnddlSearchString='catch me, if you can'"))
        64

        """

        logger.debug(
            f'__init__({self}, {gldnddlSearchString}, {start_urls}, {option}, {args}, {kwargs})')
        if option not in ['None', 'regex', 'email']:
            logger.error(f'please add a valid  -a option=')
            os._exit(os.EX_USAGE)
        else:
            Gldnddl.option = option
            if option == 'email':
                Gldnddl.search_expression = """(?<=\\W*)([\\w\\.(\\[dot\\]|\\.)]+?(\\[at\\]|@).+?(\\[dot\\]|\\.).+?)(?=\\W)"""
        if gldnddlSearchString is None and option != 'email':
            logger.error(
                f"please add -a gldnddlSearchString='what ever you like'")
            os._exit(os.EX_USAGE)
        else:
            if gldnddlSearchString != None:
                Gldnddl.search_expression = str(gldnddlSearchString).lower()
        logging.info('Gldnddl.option: %s, Gldnddl.search_expression: %s',
                     Gldnddl.option, Gldnddl.search_expression)
        if start_urls is None:
            logger.error(
                f"please add -a start_urls='https:search.xy'")
            os._exit(os.EX_USAGE)
        else:
            self.start_urls = start_urls.split(",")
            logger.info(f"self.start_urls: {self.start_urls}")
        allowed = set()  # define allowed as `set()` to keep every domain only once
        for url in self.start_urls:
            extract = tldextract.tldextract.extract(url)
            allowed.add(extract.domain +
                        "." + extract.suffix)

        self.allowed_domains = list(allowed)
        logger.info(f"self.allowed_domains: {self.allowed_domains}")

        # Set up deny list
        # Adding the pinterest and tumblr deny rules to prevent urls such as the following being indexed e.g. for example.com
        # https://www.pinterest.com/pin/create/button/?url=https%3A%2F%2Fexample.com...
        # https://www.tumblr.com/widgets/share/tool/preview?shareSource=legacy&canonicalUrl=&url=https%3A%2F%2Fexample.com%2F
        # These seem to be triggered by links on the original domain such as
        # https://example.com/page/?share=pinterest
        deny = [r'.*\?share\=pinterest.*', r'.*\?share\=tumblr.*']

        self.rules = (
            Rule(
                LinkExtractor(allow_domains=self.allowed_domains,
                              deny=deny, deny_extensions=IGNORED_EXTENSIONS),
                callback="parse_item", follow=True
            ),
        )
        logger.debug(f"End of Goldendoodle's __init__ overwrite.")
        super().__init__()

    def parse_start_url(self, response, **kwargs):
        """Parse the start URL as all other URLs.

        Args:
            response (_type_): Fetch return code and URL

        Yields:
            Scrapy Respons object: see https://docs.scrapy.org/en/latest/topics/request-response.html?highlight=response#response-objects

        A search in: https://example.com/ for 'Example' should result in
        ================================================================

        >>> file = 'reports/findings.json';
        >>> if os.path.exists(file):
        ...     os.remove(file)
        >>> os.system(f"scrapy crawl recherchedechaîne_gldnddl -O reports/findings.json -a gldnddlSearchString='Example' -a start_urls=https://example.com/")
        0
        >>> import json
        >>> with open('reports/findings.json') as findingsreport:
        ...     findings = json.load(findingsreport)[0]
        ...     findings['regex_findingElementsQuery']
        "['/html/head/title', '/html/body/div/h1', '/html/body/div/p[1]', '/html/body/div/p[2]', '/html/body/div/p[2]/a']"

        A search in a dynamic webpage for 'ScrapingAnt' should result in
        ================================================================

        >>> file = 'reports/findings.json';
        >>> if os.path.exists(file):
        ...     os.remove(file)
        >>> os.system(f"scrapy crawl recherchedechaîne_gldnddl -O {file} -a gldnddlSearchString='Goldendoodle' -a start_urls=https://model-enact-analyze-manage.de/souverain/index.php/dynamic-web-page-example-for-scrapy-tests/")
        0
        >>> import json
        >>> try:
        ...     with open('reports/findings.json') as findingsreport:
        ...         findings = json.load(findingsreport)[0]
        ...         findings['currentURL'][0:48]
        ... except:
        ...     pass
        'https://model-enact-analyze-manage.de/souverain/'

        A search in a webpage calling scripts should result in
        ======================================================

        >>> file = 'reports/findings.json';
        >>> if os.path.exists(file):
        ...     os.remove(file)
        >>> os.system(f"scrapy crawl recherchedechaîne_gldnddl -O {file} -a gldnddlSearchString='We are unable to find the page you have requested.' -a start_urls=https://developer.ibm.com/tmp/tmphb8vfjp6.html/")
        0
        >>> import json
        >>> try:
        ...     with open('reports/findings.json') as findingsreport:
        ...         findings = json.load(findingsreport)[0]
        ...         findings['webdriver_findingElements'][3:62]
        ... except:
        ...     pass
        '<h2>we are unable to find the page you have requested.</h2>'

        """

        # parse start URL with parse_item:
        yield Request(url=response.url, callback=self.parse_item)

    def parse_item(self, response):
        """This is the Goldendoodle parser. First it checks wether the search string is in the site. If this is so, then the parser determines a xpath to every occurence of the search string. These xpath statements then are used to get the element(s) containging the search string.

        Yields: Gldnddl: The results of the parser, if any.

        For further development or testing purposes set Gldnddl.gldnddlShell = True and Goldendoodle will open a Scrapy shell for every site.

        Results will only by shown, when the site includes the search string.
                                                                                                                
        Results are either the search string itself or the capturing of an regex expression, like (?<=mailto:)(.+?)(?=\\?|"+), which delivers the (.+?)-group of the expression.

        Example of capturing group search:
        ==================================

        >>> file = 'reports/findings_208.json'
        >>> if os.path.exists(file):
        ...     os.remove(file)
        >>> logger.debug(f'''test: scrapy crawl recherchedechaîne_gldnddl -O {file} -a gldnddlSearchString='(?<=mailto:)(.+?)(?=\?|"+)' -a option=regex -a start_urls=https://model-enact-analyze-manage.de/souverain/index.php/2022/10/24/goldendoodle-turned-into-a-truffle-pig''')
        >>> os.system(f'''scrapy crawl recherchedechaîne_gldnddl -O {file} -a gldnddlSearchString='(?<=mailto:)(.+?)(?=\?|"+)' -a option=regex -a start_urls=https://model-enact-analyze-manage.de/souverain/index.php/2022/10/24/goldendoodle-turned-into-a-truffle-pig''')
        0
        >>> import json
        >>> with open(file) as findingsreport:
        ...     for finding in json.load(findingsreport):
        ...         if finding["currentURL"] == "https://model-enact-analyze-manage.de/souverain/index.php/2022/10/24/goldendoodle-turned-into-a-truffle-pig/":
        ...             str(str(finding['regex_finding']).split(',')[2]).split("'")[1]
        'melchior.im.Dreital@model-enact-analyze-manage.de'

        """
        
        # Invoke test shell
        if Gldnddl.invoke_shell == True:
            # FUTUREFEATURE: For further development or testing purposes set Gldnddl.gldnddlShell = True and Goldendoodle will open a Scrapy shell for every site.
            from scrapy.shell import inspect_response
            inspect_response(response, self)
        # Settings
        currentURL = str(response.request.url)
        logger.debug(f"currentURL:{currentURL}")
        currentHeaders = str(response.headers)
        #   ############    #
        #   regex search    #
        #   ############    #
        try:
            logger.debug(
                f"Gldnddl.search_expression:{Gldnddl.search_expression}:flags:{regex.IGNORECASE|regex.MULTILINE|regex.DOTALL}:response.text:{response.text}:")
            regex_finding = regex.search(Gldnddl.search_expression, response.text, regex.IGNORECASE|regex.DOTALL)
        except:  # p.e. https://www.bombini-verlag.de/j/shop/withdrawalpdfdownload is at least a pdf-file
            raise
        # Prepare findings from Scrapy regex
        # Elements from scrapy-response.body will only by shown, when the site includes the search string.
        regex_searchpath = gu.set_searchpath(
            regex_finding, Gldnddl.search_expression)
        try:
            (regex_findingElementsQuery, regex_findingElements) = gu.determineFindingElementsQuery(
            currentURL, regex_searchpath, response.body)
        except:
            regex_findingElementsQuery = 'Error see errlog'
            regex_findingElements = ['Error see errlog']
        #   --------------------------------------- #
        #   inner HTML of Selenium Chrome webdriver #
        #   --------------------------------------- #
        # Try to read with Selenium webdriver
        (etreePageSource, stringresponsebody, webdriver_finding, cleared_webdriver_finding) = gu.read_with_webdriver(currentURL, Gldnddl.search_expression)
        # Prepare findings from Selenium
        # findingElementsQuery with results from Selenium webdriver
        webdriver_searchpath = gu.set_searchpath(
            webdriver_finding, Gldnddl.search_expression)
        (webdriver_findingElementsQuery, webdriver_findingElements) = gu.determineFindingElementsQuery(currentURL, webdriver_searchpath, stringresponsebody)
        #   ################################################################    #
        #   clearedfindingElementsQuery with results from Selenium webdriver    #
        #   ################################################################    #
        cleared_webdriver_searchpath = gu.set_searchpath(
            cleared_webdriver_finding, Gldnddl.search_expression)
        (cleared_webdriver_findingElementsQuery, cleared_webdriver_findingElements) = gu.determineFindingElementsQuery(
            currentURL, cleared_webdriver_searchpath, stringresponsebody)
        #   ####################### #
        #   assemble search results #
        #   ####################### #
        gldnddlI = gi.GoldendoodleItem()
        gldnddlI['currentURL'] = currentURL
        gldnddlI['currentHeaders'] = currentHeaders
        gldnddlI['regex_finding'] = str(regex_finding)
        gldnddlI['regex_findingElements'] = str(regex_findingElements)
        gldnddlI['regex_findingElementsQuery'] = str(
            regex_findingElementsQuery)
        gldnddlI['webdriver_finding'] = str(webdriver_finding)
        gldnddlI['webdriver_findingElements'] = str(webdriver_findingElements)
        gldnddlI['webdriver_findingElementsQuery'] = str(
            webdriver_findingElementsQuery)
        gldnddlI['cleared_webdriver_finding'] = str(cleared_webdriver_finding)
        gldnddlI['cleared_webdriver_findingElements'] = str(
            cleared_webdriver_findingElements)
        gldnddlI['cleared_webdriver_findingElementsQuery'] = str(
            cleared_webdriver_findingElementsQuery)

        yield gldnddlI
