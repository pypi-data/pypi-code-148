#!%PYTHON_HOME%\python.exe
# coding: utf-8
# version: python38

from collections.abc import Iterable
from functools import reduce

from yutils.exceptions import WrongDatatype, InputError
from yutils.tools.str import turn_numeric


np = None
def _import_numpy():
    global np
    if np is None:
        from yutils._import import import_numpy
        np = import_numpy()
pd = None
def _import_pandas():
    global pd
    if pd is None:
        from yutils._import import import_pandas
        pd = import_pandas()


class NPConstants(object):
    def __init__(self):
        _import_numpy()

    @property
    def TWO_D_ARRAY_TYPE(self):
        return ([list, tuple, np.ndarray],
                [list, tuple, np.ndarray])

    @property
    def TWO_D_ARRAY_INTS_FLOATS_TYPE(self):
        return ([list, tuple, np.ndarray],
                [list, tuple, np.ndarray],
                [int, float, np.integer, np.floating])

    @property
    def TWO_D_NP_ARRAY_INTS_FLOATS_TYPE(self):
        return (np.ndarray, np.ndarray, [np.integer, np.floating])

    @property
    def TWO_D_ARRAY_INTS_TYPE(self):
        return ([list, tuple, np.ndarray],
                [list, tuple, np.ndarray],
                [int, np.integer])


def get_indices_containing_all_substrings(array, *substrings):
    _import_numpy()
    substring_found_indices = []
    for substring in substrings:
        substring_found_indices.append(np.where(np.array([i.find(substring)
                                                          if isinstance(i, str) else -1
                                                          for i in array]) != -1)[0])
    return reduce(np.intersect1d, substring_found_indices)


def to_array(obj, turn_str_items_to_numeric=False):
    _import_numpy()
    _import_pandas()

    if not is_iterable(obj):
        raise WrongDatatype(obj, Iterable, type(obj))
    if isinstance(obj, np.ndarray):
        return obj
    if isinstance(obj, (pd.DataFrame, pd.Series)):
        return obj.to_numpy()

    if len(obj) > 0 and is_iterable(obj[0]):
        return np.array([to_array(item, turn_str_items_to_numeric) for item in obj])
    else:
        if turn_str_items_to_numeric:
            return np.array([turn_numeric(item) for item in obj])
        return np.array(obj)


def is_iterable(obj):
    return isinstance(obj, Iterable) and not isinstance(obj, str)


def normalize_array(array, axis=None):
    _import_numpy()

    mu = np.mean(array, axis=axis)
    sigma = np.std(array, axis=axis)
    if isinstance(sigma, np.ndarray):
        sigma[sigma == 0] = 1
    else:
        sigma = sigma if sigma else 1
    normalized_array = (array - mu) / sigma
    return normalized_array, mu, sigma


def r2c(array):
    _import_numpy()

    if len(array.shape) == 1:
        return array[:, np.newaxis]
    elif array.shape[1] == 1:
        return array
    elif array.shape[0] == 1:
        return array[0][:, np.newaxis]
    raise InputError(f'Input of shape {array.shape} should be array but is multi dimensional matrix.')


def magic(n):
    """
    Implementation taken from https://stackoverflow.com/questions/47834140/numpy-equivalent-of-matlabs-magic
    from user: user6655984
    """
    _import_numpy()

    n = int(n)
    if n < 3:
        raise ValueError("Size must be at least 3")
    if n % 2 == 1:
        p = np.arange(1, n+1)
        return n*np.mod(p[:, None] + p - (n+3)//2, n) + np.mod(p[:, None] + 2*p-2, n) + 1
    elif n % 4 == 0:
        J = np.mod(np.arange(1, n+1), 4) // 2
        K = J[:, None] == J
        M = np.arange(1, n*n+1, n)[:, None] + np.arange(n)
        M[K] = n*n + 1 - M[K]
    else:
        p = n//2
        M = magic(p)
        M = np.block([[M, M+2*p*p], [M+3*p*p, M+p*p]])
        i = np.arange(p)
        k = (n-2)//4
        j = np.concatenate((np.arange(k), np.arange(n-k+1, n)))
        M[np.ix_(np.concatenate((i, i+p)), j)] = M[np.ix_(np.concatenate((i+p, i)), j)]
        M[np.ix_([k, k+p], [0, k])] = M[np.ix_([k+p, k], [0, k])]
    return M


def get_variables_from_mat_file(file_path, variable_names=None, verbose=True):
    """
    Return specific variables from a mat file (so that you don't have to unpack the dict returned by scipy.io.loadmat

    :param file_path: path of your .mat file
    :type file_path: str
    :param variable_names: names of variables you want to return, in order
    :default variable_names: None
    :type variable_names: list of str
    :param verbose: If to print version, time of file creation and number of global variables
    :default verbose: True
    :type verbose: bool

    :return: variables stored in .mat file
    :return len: len(variable_names)
    """
    from scipy.io import loadmat

    HEADERS = ['__header__', '__version__', '__globals__']
    all_data = loadmat(file_path)
    variable_data = {key: value for key, value in all_data.items() if key not in HEADERS}

    if verbose:
        print(all_data[HEADERS[0]])
        print('Version:', all_data[HEADERS[1]])
        print(f'With {len(all_data[HEADERS[2]])} globals')
        print(f'Found {len(variable_data)} variables:', list(variable_data.keys()))

    if not variable_names:
        return variable_data
    return tuple(variable_data[var] for var in variable_names)


def is_matrix(array):
    return len(array.shape) > 1


def isnt_column_array(array):
    return min(array.shape) != 1

