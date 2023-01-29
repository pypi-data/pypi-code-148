#!%PYTHON_HOME%\python.exe
# coding: utf-8
# version: python38


import numpy as np

from yutils.exceptions import InputError
from yutils.tools.numpy_tools.numpy_tools import to_array, is_matrix


def gaussian_parameter_estimation(data):
    """
    Creates inputs for AnomalyProbability.

    In order to catch correlations between features,
    you must create a new feature by yourself,
    or else use the gaussian_parameter_estimation_multivariate.

    Can be used even if n is very large (not many features)
        and also if m <= n (no need for covariance matrix)
    """
    data = to_array(data)
    mu = np.mean(data, axis=0)
    sigma_squared = np.mean((data - mu) ** 2, axis=0)
    return mu, sigma_squared


class AnomalyProbability(object):
    """
    Use inputs from gaussian_parameter_estimation.

    In order to catch correlations between features,
    you must create a new feature by yourself,
    or else use the AnomalyProbabilityMultivariate.

    Can be used even if n is very large (not many features)
        and also if m isn't much greater than n (no need for covariance matrix)
    """
    _SQRT_2_PI = np.sqrt(2 * np.pi)

    def __init__(self, mu, sigma_squared):
        self.mu = mu
        self.sigma_squared = sigma_squared
        self._sigma = None

        if isinstance(mu, (int, float)) and isinstance(sigma_squared, (int, float)):
            self._dimensions = 1
        elif len(mu) == len(sigma_squared):
            self._dimensions = len(mu)
        else:
            raise InputError("Inputs 'mu' and 'sigma_squared' aren't same length")

    @property
    def sigma(self):
        if self._sigma is None:
            self._sigma = np.sqrt(self.sigma_squared)
        return self._sigma

    def prob(self, example):
        if is_matrix(example):
            return np.apply_along_axis(self.prob, 1, example)

        self._check(example)

        first = 1 / (self._SQRT_2_PI * self.sigma)
        second = np.exp(- ((example - self.mu) ** 2) / (2 * self.sigma_squared))

        return np.product(first * second)

    def _check(self, example):
        if isinstance(example, (int, float)) and self._dimensions == 1:
            return

        if len(example) == self._dimensions:
            return

        raise InputError(f"Example given should have {self._dimensions} dimensions")


def gaussian_parameter_estimation_multivariate(data):
    """
    Creates inputs for AnomalyProbabilityMultivariate.

    Also automatically catches correlations between features!

    To be used when m > n (or else covariance matrix will be non-invertable)
    and if n isn't very large (not many features)

    If you find that the covariance matrix is non-invertable,
     it is either because:
    a) m isn't a lot bigger than n
    b) you have redundant features (linearly dependant)
        look for them and remove them
    """
    data = to_array(data)
    mu = np.mean(data, axis=0)
    covariance_matrix = np.cov(data.T)
    return mu, covariance_matrix


class AnomalyProbabilityMultivariate(object):
    """
    Use inputs from gaussian_parameter_estimation_multivariate.

    Also automatically catches correlations between features!

    To be used when m >> n (or else covariance matrix will be non-invertable)
     ( let's say only when one of these is true:
        m >= 10 * n
        m >= (n ** 2) / 2
      )
    and if n isn't very large (not many features)

    If you find that the covariance matrix is non-invertable,
     it is either because:
    a) m isn't a lot bigger than n
    b) you have redundant features (linearly dependant)
        look for them and remove them
    """
    def __init__(self, mu, covariance_matrix):
        self.mu = mu
        self.covariance_matrix = covariance_matrix

        self._determinant = None

        if len(mu) == covariance_matrix.shape[0] == covariance_matrix.shape[1]:
            self._dimensions = len(mu)
        else:
            raise InputError("Inputs 'mu' and 'covariance_matrix' "
                             "don't have the same dimensions.")

    @property
    def determinant(self):
        if self._determinant is None:
            self._determinant = np.linalg.det(self.covariance_matrix)
        return self._determinant

    def prob(self, example):
        if is_matrix(example):
            return np.apply_along_axis(self.prob, 1, example)

        self._check(example)

        first = 1 / (
                ((2 * np.pi) ** (self._dimensions / 2))
                * (self.determinant ** 0.5)
        )
        second = np.exp(-0.5 *
                        (example - self.mu).T
                        @ np.linalg.inv(self.covariance_matrix)
                        @ (example - self.mu)
                        )

        return first * second

    def _check(self, example):
        if len(example) == self._dimensions:
            return

        raise InputError(f"Example given should have {self._dimensions} dimensions")


def select_threshold(training_values, probabilities):
    """
    This function finds the best epsilon, using training values of a cross-validation set and their probabilities.

    :param training_values: 0's and 1's, if training_data is an anomaly or not
    :type training_values: array
    :param probabilities: The probabilities that training_data is an anomaly, given by AnomalyProbability.prob
    :type probabilities: array

    :return: the best epsilon found
    :rtype: float
    """
    best_epsilon = 0
    best_f1 = 0

    if len(training_values.shape) == 2 and training_values.shape[1] == 1:
        training_values = training_values[:, 0]

    for epsilon in np.linspace(np.min(probabilities), np.max(probabilities), 1000):
        flagged_anomalies = probabilities < epsilon

        predicted_positives = sum(flagged_anomalies == 1)
        actual_positives = sum(training_values == 1)
        correct_positives = np.sum(np.logical_and(training_values == 1, flagged_anomalies == 1))

        if predicted_positives > 0 and actual_positives > 0:
            precision = correct_positives / predicted_positives
            recall = correct_positives / actual_positives
            f1 = (2 * precision * recall) / (precision + recall)
        else:
            f1 = 0

        if f1 > best_f1:
            best_f1 = f1
            best_epsilon = epsilon

    return best_epsilon
