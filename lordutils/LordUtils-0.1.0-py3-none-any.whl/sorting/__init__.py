from ..regs.patterns import pattern_number


def __get_key(var):
    key = pattern_number.findall(var)
    key = [int(numeric_string) for numeric_string in key]
    return key


def sort_numeric(items, preformat=None):
    """Sorted lists based on the number contained in the items"""
    if preformat is None:
        pre_f = __get_key
    else:
        pre_f = lambda x: __get_key(preformat(x))
    return sorted(items, key=pre_f)
