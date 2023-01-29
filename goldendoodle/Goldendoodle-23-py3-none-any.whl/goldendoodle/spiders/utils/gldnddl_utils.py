import logging
import sys
from datetime import datetime
from distutils.filelist import findall
from inspect import currentframe, getframeinfo
from lib2to3.pgen2 import driver
from logging import exception
from random import random
from re import IGNORECASE
from typing import Union, Tuple


import regex    
from lxml import etree
from lxml.html.soupparser import fromstring
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys

logger = logging.getLogger(__name__)

def read_with_webdriver(url: str, search_string: str) -> Tuple[str, str, str, str]:
    """Read site again with Selenium webdriver

    Args:
        url (str): response.request.url from scrapy
        search_string (str): search string

    Returns:
        Any: site html as etree
        str: site html
        Match[str]: finding, if any
        Match in cleared web site[str]: finding, if any
        
    """
    logger.debug(f'read_with_webdriver("{url}", "{search_string}")')
    _options = webdriver.ChromeOptions()
    _options.headless = True
    _options.add_argument("start-maximized")
    _options.add_experimental_option("excludeSwitches", ["enable-automation"])
    _options.add_experimental_option('useAutomationExtension', False)
    _driver = webdriver.Chrome(
        ChromeDriverManager().install(), options=_options)
    _wait_time = 23  # seconds FUTUREFEATURE variable
    _driver.implicitly_wait(max(_wait_time/11, random()*_wait_time, 13))
    _driver.get(url)
    # scroll to the bottom of a page
    _driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    # initiate while loop
    _newInnerHTML = 'init inner HTML'
    _start_time = datetime.now()
    _etree_page_source = None 
    _inner_HTML = None
    _webdriver_finding = None
    _cleared_webdriver_finding = None
    while True:
        _huge_tree_parser = etree.XMLParser(recover=True, huge_tree=True)
        try:
            _etree_page_source = etree.fromstring(
                _driver.page_source, parser=_huge_tree_parser)
            _element = _driver.find_element(By.TAG_NAME, "html")
            _inner_HTML = _element.get_attribute('innerHTML')
        except:
            raise
        _string = str(_inner_HTML)
        _webdriver_finding = regex.search(
            search_string, _string, regex.IGNORECASE)
        # try search again, but with some changes of the site code which might resolve some obfuscations
        # clear
        _string = regex.sub('\\[ät\\]', '@', regex.sub('\\[at\\]', '@', regex.sub('\\[dot\\]', '.', regex.sub(
            "<!--[\\s\\S]*?-->", "", _string), flags=regex.IGNORECASE), flags=regex.IGNORECASE), flags=regex.IGNORECASE)
        _cleared_webdriver_finding = regex.search(
            search_string, _string, regex.IGNORECASE)
        _time_delta = datetime.now() - _start_time
        if (_time_delta.total_seconds() > _wait_time*3 and _newInnerHTML == _inner_HTML) or _webdriver_finding != None or _cleared_webdriver_finding != None:
            break
        else:
            _newInnerHTML = _inner_HTML
    logger.debug(
        f'read_with_webdriver return {_etree_page_source}, {str(_inner_HTML)}, {_webdriver_finding}, {_cleared_webdriver_finding}')
    return str(_etree_page_source), str(_inner_HTML), str(_webdriver_finding), str(_cleared_webdriver_finding)


def determineFindingElementsQuery(currentURL, searchpath, responsebody):
    """Determine all the queries to all the findings 

    Args:
        currentURL (_type_): URL of the current site
        searchpath (Any): xpath to the first occurence of the search string
        responsebody (Any): site HTML

    Returns:
        _type_: _description_
        str: xpath queries to all findings
        list: list of all found XML elements
    """
    logger.debug(
        f'determineFindingElementsQuery({currentURL}, {searchpath}, {responsebody})')
    _str_responsebody = str(responsebody)
    try:
        if Gldnddl.option in ['regex', 'email']:
            _etree_responsebody = fromstring(_str_responsebody)
        else:
            _etree_responsebody = fromstring(
                str(_str_responsebody).lower())
    except ValueError:
        logger.error(
            f'ValueError in {currentURL} _str_responsebody: {_str_responsebody}')
        raise ValueError
    except:
        raise
    try:
        _tree_responsebody = etree.ElementTree(
            _etree_responsebody)
    except Exception:
        raise ValueError(responsebody)
    try:
        _compiledXPATH = etree.XPath(searchpath)
    except Exception:
        raise SyntaxError(searchpath)
    try:
        _findingElementsQuery = str([_tree_responsebody.getpath(
            _pathToElement.getparent()) for _pathToElement in _compiledXPATH(_tree_responsebody)])
    except Exception:
        raise ValueError(_tree_responsebody,
                         _compiledXPATH)

    # findingElements:
    treeresponsebody = etree.ElementTree(_etree_responsebody)
    xps = getparentForFindingElements(
        _tree_responsebody, _compiledXPATH)
    findingElements = determineFindingElements(
        xps, treeresponsebody)
    logger.debug(
        f'determineFindingElementsQuery return {_findingElementsQuery}, {findingElements}')
    return (_findingElementsQuery, findingElements)


def getparentForFindingElements(tree_responsebody, xpath_searchdefinition):
    """get the XML parent element of the finding

    Args:
        tree_responsebody (Any): etree to search in
        xpath_searchdefinition (Any): XML path leading to search string

    Returns:
        list: list of XML path(es) to parent element(s)
    """
    
    logger.debug(
        f'getparentForFindingElements({tree_responsebody}, {xpath_searchdefinition})')
    try:
        xps = [tree_responsebody.getpath(text.getparent(
        )) for text in xpath_searchdefinition(tree_responsebody)]
    except Exception:
        raise
    logger.debug(f'getparentForFindingElements -> {xps}')
    return xps


def determineFindingElements(xps, tree_responsebody):
    """determine all XML element with findings

    Args:
        xps (Any): XML path(es) to finding(s)
        tree_responsebody (Any): etree of site

    Returns:
        list: list of element(s) with finding(s)
    """

    logger.debug(
        f'determineFindingElements({xps}, {tree_responsebody})')
    findingElements = []
    for xp in xps:
        xpathsearchdefinition = etree.XPath(xp)
        findingElement = ''
        try:
            findingElement = xpathsearchdefinition(
                tree_responsebody)[0].tail.strip()
        except Exception:
            try:
                findingElement = etree.tostring(xpathsearchdefinition(
                    tree_responsebody)[0])
            except Exception:
                logging.exception(
                    '2. except, repr(Exception) = %s, xp = %s', repr(Exception), xp)
                findingElement = xp
        finally:
            findingElements.append(findingElement)
    logger.debug(f'determineFindingElements -> {findingElements}')
    return findingElements


def set_searchpath(finding, search_expression):
    """Set the searchpath depending on whether the search string is a regular expression or not.

    Args:
        finding (Any): A list of the findings.If the search string is a regular expression, just the first finding will be used in the xpath.
        search_expression (Any): The search string.

    Returns:
        Any: A xpath to the parent element of the finding
    """
    logger.debug(f'set_searchpath({finding}, {search_expression})')
    if Gldnddl.option in ['regex', 'email']:
        if finding is None:
            # result has to be a valid xpath statement
            to_be_find = ".."
        else:
            # --> https://www.jochentopf.com/email/chars.html
            email_chars = '''[\\w\\d\\.\\-\\&\\'\\*\\+\\/\\=\\?\\^\\_\\{\\}\\~]'''
            at_string = regex.search(
                f'{email_chars}*@{email_chars}*', finding[0])
            if Gldnddl.option in ['email'] and at_string:
                to_be_find = at_string[0]
            else:
                to_be_find = finding[0]
    else:
        to_be_find = search_expression
    searchpath = "//text()[contains(.,'" + to_be_find + "')] | //meta/@content[contains(.,'" + \
        to_be_find + \
        "')] | //*[@*[contains(.,'" + \
        to_be_find + \
        "')]] | //a/@href[contains(.,'" + to_be_find + "')]"
    logger.debug(f'set_searchpath -> {searchpath}')
    return searchpath


class Gldnddl:
    """Variables for global use
    """
    search_expression: str = ""
    invoke_shell: bool = False
    option: str = 'False'