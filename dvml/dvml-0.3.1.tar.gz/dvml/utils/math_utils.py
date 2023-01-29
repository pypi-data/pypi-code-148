"""
Utility functions for math operations
"""
import numpy as np


def sigmoid(x_in):
    """
    Computes the sigmoid function for each value of an array

    :param x_in: numpy array (or equivalent)
    :return: numpy array with value of sigmoid function for each element of x_in
    """
    sig = 1 / (1 + np.exp(-np.array(x_in)))

    return sig
