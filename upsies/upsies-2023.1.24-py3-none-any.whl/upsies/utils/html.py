"""
HTML parsing
"""

import re

from . import LazyModule

bs4 = LazyModule(module='bs4', namespace=globals())


def parse(string):
    """
    Return :class:`~.bs4.BeautifulSoup` instance

    :param string: HTML document

    :raise ContentError: if `string` is invalid HTML
    """
    if isinstance(string, bs4.element.Tag):
        return string
    else:
        return bs4.BeautifulSoup(string, features='html.parser')


def dump(html, filepath):
    """
    Write `html` to `filepath` for debugging

    :param html: String or :class:`~.bs4.BeautifulSoup` instance
    """
    with open(filepath, 'w') as f:
        if isinstance(html, bs4.BeautifulSoup):
            f.write(html.prettify())
        else:
            f.write(parse(str(html)).prettify())


def as_text(html):
    """Strip HTML tags from string and return text without markup"""
    text = parse(html).get_text()
    text = re.sub(r'(\s)\s+', r'\1', text, flags=re.MULTILINE).strip()
    return text


def purge_javascript(html):
    """
    Return `html` with <script> tags removed

    :param str html: HTML string
    """
    soup = parse(html)
    for script_tag in soup.find_all('script'):
        script_tag.decompose()
    return str(soup)
