import regex as re
import validators
from fnmatch import fnmatchcase as fnmatch
from ..regs.patterns import pattern_number


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


def convert_to_int(value: str | None, default=None):
    if value is None:
        return default

    if value.isdigit():
        return int(value)

    value = re.sub('^([^0-9]*)([0-9]+)([^0-9]*)$', r'\2', value)
    if value.isdigit():
        return int(value)

    return default


def convert_to_float(value: str | None, default=None):
    if value is None:
        return default

    try:
        r = float(value)
        return r
    except ValueError:
        pass

    value = re.sub('^([^0-9]*)([0-9.]+)([^0-9]*)$', r'\2', value)

    try:
        r = float(value)
        return r
    except ValueError:
        pass

    return default


def get_numbers_from_string(var: str):
    numbers = pattern_number.findall(var)
    numbers = [int(numeric_string) for numeric_string in numbers]
    return numbers
