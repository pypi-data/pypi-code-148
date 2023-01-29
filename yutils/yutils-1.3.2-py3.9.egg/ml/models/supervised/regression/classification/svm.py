#!%PYTHON_HOME%\python.exe
# coding: utf-8
# version: python38

import warnings
import decimal
from decimal import Decimal
decimal.setcontext(decimal.BasicContext)
import numpy as np
from sklearn import svm

from yutils.exceptions import InputError
from yutils.tools.numpy_tools import r2c, is_matrix
from yutils.ml.models.supervised.regression.classification.classification import Classification


class SVM(Classification):
    DEFAULT_GAMMA = 'scale'
    DEFAULT_ITERATIONS = -1
    DEFAULT_KERNEL = 'rbf'  # Which is practically a Gaussian Kernel
    ALTERNATIVE_KERNEL = 'linear'

    _SVM_EXTRA_INPUT_TYPES = dict(C=[type(None), int, float],
                                  sigma=[type(None), int, float, str],
                                  gamma=[type(None), int, float, str],
                                  kernel=str)

    _SVM_EXTRA_INPUT_DEFAULTS = dict(C=None,
                                     sigma=None,
                                     gamma=None,
                                     iterations=DEFAULT_ITERATIONS,
                                     kernel=DEFAULT_KERNEL)
    _SPECIAL_GAMMA_SIGMA_VALUES = ['auto', 'scale']
    
    _CHANGE_TO_CONSTANT_INPUTS = dict(regularization=True,
                                      use_optimized_gradient_descent=True,
                                      gradient_checking=False,
                                      optimization_method=None,
                                      learning_rate=0.0,
                                      try_recommended_optimization_methods=False)
    _CONSTANT_INPUTS_WARNING = 'Invalid input: {key}={inp} : {key} must always be {const} for SVM Classifier. Input {key} changed to {const}.'


    def __init__(self, training_data, training_results, **kwargs):
        """
        Creates a regression object, for use in linearization/classification problems.

        :param training_data: Data to train algorithm to - columns are features and rows are training examples
                                Column of ones should already be added as first column
        :type training_data: 2-D numpy array
        :param training_results: Results of each training algorithm
        :type training_results: numpy array

        :param kwargs: Additional keyword arguments


            Available keyword arguments:

        :param kernel: Specifies the kernel type to be used in the algorithm. Usually you'll want either "rbf" (gaussian) or "linear".
        :default kernel: "rbf", or in other words a gaussian kernel
        :type kernel: str

        :param C: Regularization parameter. The strength of the regularization is inversely proportional to C. Must be strictly positive.
                  The weight to give the feature cost for regularized gradient descent.
                    This is inversely proportinal to regularization_lambda (1/self.regularization_lambda if C is None)
                      A smaller value will prevent overfitting in that it prevents theta values for
                      irrelevant features from growing. Too small a value though can create underfitting.
        :default C: None - will default to 1
        :type C: int or float

        :param regularization_lambda: The weight to give the regularization term for regularized gradient descent.
                                      This is the weight of the penalization, or "tax" on the grown of theta values of features.
                                        A bigger value will prevent overfitting in that it prevents theta values for
                                        irrelevant features from growing. Too big a value though can create underfitting.
        :default regularization_lambda: 1
        :type regularization_lambda: int or float

        :param sigma: Kernel coefficient (see "rbf"/"gaussian" kernel function at the bottom of this docstring)
                        This will be converted to gamma in the cls.sigma_to_gamma() function.
        :default sigma: 'scale' (see doc for gamma to understand what this means)
        :type sigma: int, or "scale" or "auto"

        :param gamma: Kernel coefficient (see "rbf"/"gaussian" kernel function at the bottom of this docstring)
                        From sklearn.svm.SVC documentation:
                            if gamma='scale' (default) is passed then it uses 1 / (n_features * X.var()) as value of gamma,
                            if ‘auto’, uses 1 / n_features.
        :default gamma: 'scale'
        :type gamma: int, or "scale" or "auto"

        :param iterations: Number of iterations to run, use -1 for no limit
        :default iterations: -1 (no limit)
        :type iterations: int

        :param threshold: The threshold on which to classify if the prediction is a yes (1) or a no (0)
                            By default is 0.5
                            Give a higher threshold for less false positives, give a lower threshold for less false negatives.
                          You cannot give a threshold different than 0.5 if there are more than two classes in the training results.
        :default threshold: 0.5
        :type threshold: float

        :param skewed: If the data is skewed (if there are many more of one class of training data than there are of the other class
        :type skewed: bool

        :param data_editor: A function that receives new data and edits it in the same way the original data was edited
                                before being given to this class.
                            Usually, this function adds new features that need to be added (e.g. polynomial features)
                                and performs normalization on all columns based on the original data's 'sigma' and 'mu'.
        :default data_editor: None
        :type data_editor: function

        :param assess_for_warning: If to raise warnings if they emerge
        :default assess_for_warning: True
        :type assess_for_warning: bool

        :param verbose: If to print messages
        :default verbose: True
        :type verbose: bool

        :param optimizer_verbose: If the scipy optimizer/minimizer should print it's builtin optimization messages
        :default optimizer_verbose: False
        :type optimizer_verbose: bool


            # ~ * ~ * ~ *
            Some additional helper info:

            By default, this object uses an SVM with a gaussian kernel, also called "rbf" in sklearn.svm.SVC.
            Other types of kernels:
                no kernel (linear kernel):  This is useful when n is large, and m is small  (many, many features, not so many training examples)
                gaussian kernel (also choose sigma^2):  Useful when n is small, and m is large  (many training examples, but not so many features)
                polynomial kernel: x^T @ l  ^2    or   k(x, l, c, d) => (x^T @ l + c) ^d    :   This is only useful when x and l [landmarks] (all examples) are strictly non-negative
                string kernel:   Useful if features are strings
                chi-square kernel
                histogram intersection kernel
            
            
            The similarity function for gaussian kernels is:
            
            def gaussian_kernel(xi, li):
                return exp(-||xi - li||^2    / 2 sigma^2)
            
            But in sklearn.svm.SVC the gaussian kernel is:
            
            def gaussian_kernel(xi, li):
                return exp(-gamma * ||xi - li||^2)
            
            This is why I gave two options to give as inputs: sigma or gamma. I translate here between the two.


            If n (num of features) is a whole lot bigger than m (the number of training examples)
                or the other way around (for example, one is up to a thousand and the other is tens of thousands)
            Then either us Logistic Regression or an SVM without a kernel (linear kernel)

            SVMs with gaussian kernels are best used when n is small (up to 1000) and m is intermediate (up to 10,000, sometimes even up to 50,000).
        """
        self._INPUT_TYPES.update(self._SVM_EXTRA_INPUT_TYPES)
        self._INPUT_DEFAULTS.update(self._SVM_EXTRA_INPUT_DEFAULTS)
        self._change_kwargs_to_constant_inputs(kwargs)
        super().__init__(training_data=training_data,
                         training_results=training_results,
                         **kwargs)
        self.training_results = self.training_results[:, 0]  # change back to row vector because that's what svm.SVC likes...
        
        self._predict_is_by_probability = self.threshold != self.DEFAULT_THRESHOLD
        self._edit_inputs()
        self.model = svm.SVC(verbose=self.optimizer_verbose, C=self.C, gamma=self.gamma, kernel=self.kernel,
                             max_iter=self.iterations, probability=self._predict_is_by_probability)
    
    def _change_kwargs_to_constant_inputs(self, kwargs):
        tag = 'assess_for_warning'
        assess_for_warning = self._INPUT_DEFAULTS[tag] if tag not in kwargs else kwargs[tag]

        for key, value in self._CHANGE_TO_CONSTANT_INPUTS.items():
            if key in kwargs and kwargs[key] != value:
                if assess_for_warning:
                    warnings.warn(self._CONSTANT_INPUTS_WARNING.format(key=key, inp=kwargs[key], const=value))
                kwargs[key] = value
    
    def _edit_inputs(self):
        if self.C is None:
            self.C = 1 / self.regularization_lambda
        if self.gamma is None:
            if self.sigma is None:
                self.gamma = self.DEFAULT_GAMMA
            elif self.sigma in self._SPECIAL_GAMMA_SIGMA_VALUES:
                self.gamma = self.sigma
            else:
                self.gamma = self.sigma_to_gamma(self.sigma)

        if self._predict_is_by_probability and len(np.unique(self.training_results)) != 2:
            raise InputError("Cannot assign threshold other than 0.5 with multiclass classification!")

    @staticmethod
    def sigma_to_gamma(sigma):
        return float(Decimal(1) / (Decimal(2) * (Decimal(sigma) ** Decimal(2))))

    def _run_gradient_descent_optimized(self):
        self.model.fit(self.training_data, self.training_results)

    def _final_print(self):
        if self.verbose:
            error = self.get_error(self.training_data, self.training_results)
            print(f'Final Training Error - {round(error, 4)}')

    def _initialize_all_data(self):
        pass

    @classmethod
    def _hypothesis(cls, X, theta):
        raise NotImplementedError()

    @classmethod
    def compute_cost(cls, X, y, theta, regularization=True, regularization_lambda=Classification.REGULARIZATION_LAMBDA):
        raise NotImplementedError()

    def _add_cost(self, theta=None):
        raise NotImplementedError()

    def predict(self, input_data, **kwargs):
        """
        Predict an output (or column of outputs) for a given input (or set of input arrays)

        :param input_data: data for prediction
        :param theta: If you wish for a theta different than the current self.theta, you can give it here
        :param kwargs: /dev/null

        :return: prediction
        """
        data = self.data_editor(input_data)
        if not is_matrix(data):
            data = np.array([data])  # turn into matrix
        if self._predict_is_by_probability:
            # Compare threshold to probabilities of class=1, or class sorted second.
            # This is allowed because multiclass classification isn't allowed 
            # when threshold is different than self.DEFAULT_THRESHOLD, 
            # as defined by exception in self._edit_inputs()
            probabilities = self.model.predict_proba(data)[:, 1]
            prediction_indexes = (probabilities > self.threshold).astype(int)
            predictions = r2c(self.model.classes_[prediction_indexes])
        else:
            predictions = r2c(self.model.predict(data))
        return predictions

    def get_error(self, inputs, outputs):
        """
        Should compute and return the Misclassification Error of the current self.theta hypothesis

        :param inputs: test info (1-column-padded)
        :type inputs: 2-D array
        :param outputs: test results (answers)
        :type outputs: column array
        """
        if self.skewed:
            return self.get_f_score(inputs, outputs)
        
        data = self.data_editor(inputs)
        return 1 - self.model.score(data, outputs)
