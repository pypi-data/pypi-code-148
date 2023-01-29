
from ..utils import get_numbers_from_string


def sort_numeric(items, preformat=None):
    """Sorted lists based on the number contained in the items"""
    if preformat is None:
        pre_f = get_numbers_from_string
    else:
        pre_f = lambda x: get_numbers_from_string(preformat(x))
    return sorted(items, key=pre_f)
