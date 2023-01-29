#!%PYTHON_HOME%\python.exe
# coding: utf-8
# version: python38

from yutils._import import import_numpy; np = None
from yutils.tools import basic_plot
from yutils.ml.base.ml_base import MLObject
from yutils.ml.data.features import FeatureNormalizer


class PCA(MLObject):
    """
    Principal Component Analysis
    """
    def __init__(self, input_data, features_already_normalized=False, verbose=True):
        global np
        np = import_numpy()
        super().__init__(original_input_data=input_data,
                         input_data=input_data,
                         features_already_normalized=features_already_normalized,
                         verbose=verbose)

        self._normalizer = None
        self._normalize()

        self.m, self.n = self.input_data.shape

        self.__covariance_matrix = None
        self.__U, self.__S, self.__V = None, None, None
        self.__S_sum = None

    def _normalize(self):
        if self._normalizer is None and not self.features_already_normalized:
            self._normalizer = FeatureNormalizer(self.input_data)
            self.input_data = self._normalizer.normalize()

    @property
    def _covariance_matrix(self):
        if self.__covariance_matrix is None:
            self.__covariance_matrix = self.input_data.T @ self.input_data / self.m
        return self.__covariance_matrix

    @property
    def _Sigma(self):
        return self._covariance_matrix

    def _run_singular_value_decomposition(self):
        self.__U, self.__S, self.__V = np.linalg.svd(self._covariance_matrix)

    @property
    def _U(self):
        if self.__U is None:
            self._run_singular_value_decomposition()
        return self.__U

    @property
    def _S(self):
        if self.__S is None:
            self._run_singular_value_decomposition()
        return self.__S

    @property
    def _V(self):
        if self.__V is None:
            self._run_singular_value_decomposition()
        return self.__V

    @property
    def _eigenvectors(self):
        if self.__U is None \
         or self.__S is None \
         or self.__V is None:
            self._run_singular_value_decomposition()
        return self.__U, self.__S, self.__V

    @property
    def _S_sum(self):
        if self.__S_sum is None:
            self.__S_sum = sum(self._S)
        return self.__S_sum

    def get_U_vectors(self, dimensions):
        return self._U[:, :dimensions]

    def project_data(self, dimensions):
        Ureduce = self.get_U_vectors(dimensions)
        projected_data = self.input_data @ Ureduce
        return projected_data

    @classmethod
    def recover_data_class(cls, projected_data, eigenvectors):
        approximated_data = projected_data @ eigenvectors.T
        return approximated_data

    def recover_data(self, projected_data, eigenvectors=None):
        if eigenvectors is None:
            eigenvectors = self.get_U_vectors(projected_data.shape[1])
        return self.recover_data_class(projected_data, eigenvectors)

    def percent_retained_variance_for_dimension(self, dimension):
        return sum(self._S[:dimension]) / self._S_sum

    def get_lowest_dimension(self, threshold=0.99, plot_variation=False):
        variation_retention = []
        for dimension in range(1, self.n + 1):
            variation_retention.append(self.percent_retained_variance_for_dimension(dimension))
            if variation_retention[-1] >= threshold:
                if plot_variation:
                    self._plot_variation(np.array(variation_retention) * 100, self.n, threshold * 100)
                return dimension

    @staticmethod
    def _plot_variation(variation_retention, original_dimensions, threshold):
        basic_plot(np.arange(1, len(variation_retention) + 1),
                   variation_retention,
                   title=f'Variation Being Retained\n'
                         f'Per Projection of {original_dimensions}-D Data\n'
                         f'Up to Threshold of {threshold}%',
                   xlabel='Dimension',
                   ylabel='% of Retained Variation')

    def plot_dimension_significance(self):
        basic_plot(np.arange(1, self.n + 1),
                   self._S,
                   title=f'Significance of Each Dimension Added to Projection',
                   xlabel='Dimension # Added',
                   ylabel='Significance')
