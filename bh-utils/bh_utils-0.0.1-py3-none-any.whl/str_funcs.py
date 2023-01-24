"""
Some string routines.

For usage examples, see ``./tests/test_str_funcs.py``.
"""
def extract_session_cookie(cookie: str) -> str:
    """
    From a string which might have multiple ``name=value`` pair strings, get the value 
    for ``session`` name.

    ``name=value`` pair strings are separated by semicolon (``;``). For example:

    - csrftoken=7c4Df...zSEyl; session=6bdb9...kJcQs
    - session=84f32...uSWsc

    :param str cookie: a which contains multiple ``name=value`` pair strings.

    :return: value for ``session`` if found, otherwise ``--- No Cookie ---``.
    :rtype: str.
    """
    
    items = cookie.split(';')
    for itm in items:
        itm_cleaned = itm.strip()
        if ("session=" in itm_cleaned): return itm_cleaned[8:]
    return '--- No Cookie ---'
