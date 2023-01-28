import regex as re
import validators
from fnmatch import fnmatchcase as fnmatch


def is_image(file):
    """
    check if file has a ending like a image
    """  # Todo with endswith and list for checking
    _reg = re.compile(".(png|jpeg|jpg|gif|tif|bmp|swf|svg|webp)$", flags=re.IGNORECASE)

    if _reg.search(file):
        return True
    else:
        return False


def is_url(url):
    return validators.url(url)


def is_iterable(x):
    try:
        iter(x)
    except TypeError:
        return False
    else:
        return True


def is_float(value):
    try:
        float(value)
        return True
    except (ValueError, TypeError):
        return False


def fn_match_value(value: str, m: str | list):
    if isinstance(m, str):
        return fnmatch(value, m)
    if is_iterable(m):
        for n in m:
            if fn_match_value(value, n):
                return True
        return False


def remove_double(v: list):
    return list(dict.fromkeys(v))
