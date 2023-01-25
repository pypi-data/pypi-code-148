from typing import Iterable


def get_dont_match_prefix_regex(dont_match_prefixes: Iterable, match_prefix=''):
    """
    Generate a regular expression that matches any string that does not start with any of the prefixes in the
    `dont_match_prefixes` list and starts with the `match_prefix` (if specified).

    Example:
    >>> get_dont_match_prefix_regex(['abc', 'def'], 'ghi')
    '^(?!abc|def)^ghi'

    :param Iterable dont_match_prefixes: List of prefixes to exclude from the final regular expression.
    :param str match_prefix: Prefix to include in the final regular expression. If not specified,
        defaults to an empty string.
    :return: Generated regular expression
    :rtype: str
    """
    re_str = rf"^(?!{'|'.join(dont_match_prefixes)})"
    if match_prefix:
        re_str += rf"^{match_prefix}"
    return re_str
