# -*- coding: utf-8 -*-

"""
requests.compat
~~~~~~~~~~~~~~~

This module handles import compatibility issues between Python 2 and
Python 3.
"""

try:
    import chardet
except ImportError:
    from . import charset_normalizer as chardet

import sys

# -------
# Pythons
# -------

# Syntax sugar.
_ver = sys.version_info

import json

from urllib.parse import urlparse, urlunparse, urljoin, urlsplit, urlencode, quote, unquote, quote_plus, unquote_plus, \
    urldefrag
from urllib.request import parse_http_list, getproxies, proxy_bypass, proxy_bypass_environment, getproxies_environment
from http import cookiejar as cookielib
from http.cookies import Morsel
from io import StringIO
# Keep OrderedDict for backwards compatibility.
from collections import OrderedDict
from collections.abc import Callable, Mapping, MutableMapping
from json import JSONDecodeError

builtin_str = str
str = str
bytes = bytes
basestring = (str, bytes)
numeric_types = (int, float)
integer_types = (int,)
