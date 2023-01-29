#!%PYTHON_HOME%\python.exe
# coding: utf-8
# version: python38


import re
import numpy as np

INPUT_ERROR = "Unknown input"
LYX_MATRIX_PREFIX = r"\begin{bmatrix}"
LYX_MATRIX_SUFFIX = r"\end{bmatrix}"
LYX_ARRAY_PREFIX = r"\begin{array}"
LYX_LINE_END = "\\"
LYX_COL_DELIMITER = " & "
FRACTION_REGEX_PATTERN = r"^-?\\frac{([0-9]*)}{([0-9]*)}$"
NEGATIVE = "-"


def gaus_jordan_elimination(matrix):
    """
    This function receives a matrix and runs a Gaussian elimination/row reduction algorithm
     to receive the matrix's reduced row echelon form.

    :param matrix: the original matrix to reduce
    :type matrix: list of lists, 2-d numpy array, or multiline textual LyX code

    :return: the matrix in reduced row echelon form
    :rtype: 2-d numpy array
    """
    if isinstance(matrix, np.ndarray):
        matrix = matrix.astype(np.float)
    elif isinstance(matrix, list):
        matrix = np.array(matrix).astype(np.float)
    elif isinstance(matrix, str):
        matrix = get_matrix_from_lyx(matrix)
    else:
        raise TypeError(INPUT_ERROR)

    r = 0
    for q in range(matrix.shape[1]):
        col = matrix[:, q]
        all_rows_with_coeffs = np.where(col != 0)[0]
        leading_coefficients_indices = all_rows_with_coeffs[all_rows_with_coeffs >= r]
        if not leading_coefficients_indices.size:
            continue

        if leading_coefficients_indices[0] != r:
            swap(matrix, r, leading_coefficients_indices[0])
        if matrix[r][q] != 1:
            multiply(matrix, r, 1 / matrix[r][q])
        for row in range(matrix.shape[0]):
            if row != r and matrix[row][q] != 0:
                add(matrix, row, r, -matrix[row][q])
        r += 1
    return matrix


def get_matrix_from_lyx(matrix_code, verbose=True):
    """
    Converts a multiline string of LyX code representing a matrix into a numpy array
    """
    if not (matrix_code.startswith(LYX_MATRIX_PREFIX)
            and matrix_code.endswith(LYX_MATRIX_SUFFIX)):
        raise TypeError(INPUT_ERROR)

    matrix = matrix_code.splitlines()[:-1]
    if LYX_ARRAY_PREFIX in matrix[0]:
        matrix = matrix[1:]
    else:
        matrix[0] = matrix[0].replace(LYX_MATRIX_PREFIX, "")

    for i, line in enumerate(matrix):
        matrix[i] = line.rstrip(LYX_LINE_END).split(LYX_COL_DELIMITER)

        for j, num in enumerate(matrix[i]):
            matrix[i][j] = get_num_from_lyx(num)

    result = np.array(matrix)
    if verbose:
        print("Matrix created:")
        print(result)
    return result


def get_num_from_lyx(num_code):
    """
    This function returns the LyX code into a proper number, 
     dealing with fractions and negatives if need be.
    """
    is_fraction = re.findall(FRACTION_REGEX_PATTERN, num_code)
    if is_fraction:
        fraction = float(is_fraction[0][0]) / float(is_fraction[0][1])
        if num_code[0] == NEGATIVE:
            return -fraction
        return fraction
    else:
        return float(num_code)


def print_matrix(func):
    """
    A decorator for elementary function steps that prints the stages of the algorithm
    """

    def wrapper(matrix, *args, **kwargs):
        func(matrix, *args, **kwargs)
        print()
        print(func.__name__, *args)
        print(matrix)

    return wrapper


@print_matrix
def swap(matrix, row1ind, row2ind):
    """
    This function swaps between two rows in a matrix
    """
    matrix[[row1ind, row2ind]] = matrix[[row2ind, row1ind]]


@print_matrix
def multiply(matrix, row, c):
    """
    This function multiplies a row in a matrix by a given number c
    """
    matrix[row] = c * matrix[row]


@print_matrix
def add(matrix, row_to_change, row_to_add, c):
    """
    This function adds to a row in a matrix c times another row in the matrix.
    """
    matrix[row_to_change] = matrix[row_to_change] + (c * matrix[row_to_add])
