#!%PYTHON_HOME%\python.exe
# coding: utf-8
# version: python38

from functools import partial

from yutils._import import import_numpy; np = None
from yutils.exceptions import InputError

from yutils.tools.numpy_tools import r2c, NPConstants
from yutils.tools import prioritize_dicts

from yutils.ml.models.supervised.regression.continuous.continuous import Continuous
from yutils.ml.models.supervised.supervised_model import Supervised


class CollaborativeFiltering(Continuous):
    _INPUT_TYPES = dict(original_training_data=None,
                        R=None,
                        num_features=int,
                        verbose=bool,
                        optimizer_verbose=bool,
                        iterations=int,
                        regularization=bool,
                        regularization_lambda=[int, float],
                        optimization_method=[type(None), str],
                        try_recommended_optimization_methods=bool)

    _INPUT_DEFAULTS = dict(verbose=True,
                           optimizer_verbose=False,
                           iterations=Continuous.DEFAULT_ITERATIONS,
                           regularization=True,
                           regularization_lambda=Continuous.REGULARIZATION_LAMBDA,
                           optimization_method=Continuous.DEFAULT_OPTIMIZATION_METHOD,
                           try_recommended_optimization_methods=True)

    _HARD_CODED_INPUTS = dict(gradient_checking=False,
                              assess_for_warning=False,
                              use_optimized_gradient_descent=True,
                              data_editor=None)

    def __init__(self, training_data, R, num_features, **kwargs):
        """
        Creates a Collaborative Filtering object, for use in Recommender Systems.
         Each row of training_data is a product you can recommend (e.g. movie, item, song...)
         Each column is a user
        R tells the algorithm which users rated which product.

        :param training_data: Dataset to train algorithm to - The information you know, for each product/user
        :type training_data: 2-D numpy array
        :param R: Binary-valued indicator matrix,
                   where R[i][j] = 1 if training_data[i][j] is given, and R[i][j] = 0 otherwise.
        :type R: 2-D numpy array
        :param num_features: The number of new features you want the collaborative filtering algorithm to create
        :type num_features: int

        :param kwargs: Additional keyword arguments


            Available keyword arguments:

        :param iterations: Number of iterations to descend
        :default iterations: cls.DEFAULT_ITERATIONS
        :type iterations: int

        :param regularization: If to regularize the gradient descent, in order to prevent overfitting of the training data.
                                This means to penalize, or "tax" the growth of theta values of features.
                                This prevents theta values of irrelevant features from growing.
        :default regularization: True
        :type regularization: bool

        :param regularization_lambda: The weight to give the regularization term for regularized gradient descent.
                                      This is the weight of the penalization, or "tax" on the grown of theta values of features.
                                        A bigger value will prevent overfitting in that it prevents theta values for
                                        irrelevant features from growing. Too big a value though can create underfitting.
        :default regularization_lambda: 1
        :type regularization_lambda: int or float

        :param optimization_method: Name of scipy.optimize.minimize optimization method to use for minimization of
                                    cost function.
                                    Will be ignored if use_optimized_gradient_descent is False.
                                    Reccommendation: "TNC" (Truncated Newton method) for regression with few theta values,
                                                     "CG" (Conjugate Gradient) for regression with huge theta value matrices
                                                     "BFGS" is another option for short thetas, but sometimes raises warnings
        :default optimization_method: default or None will use the default scipy.optimize.minimize (usually BFGS)
        :type optimization_method: str

        :param try_recommended_optimization_methods: If scipy.optimize.minimize raises a known error,
                                                        and I can recommend a new optimization method instead,
                                                        try it automatically.
        :default try_recommended_optimization_methods: True
        :type try_recommended_optimization_methods: bool

        :param verbose: If to print messages
        :default verbose: True
        :type verbose: bool

        :param optimizer_verbose: If the scipy optimizer/minimizer should print it's builtin optimization messages
        :default optimizer_verbose: False
        :type optimizer_verbose: bool
        """
        global np
        np = import_numpy()
        self._INPUT_TYPES['original_training_data'] = NPConstants().TWO_D_ARRAY_INTS_FLOATS_TYPE
        self._INPUT_TYPES['R'] = NPConstants().TWO_D_ARRAY_INTS_TYPE

        super(Supervised, self).__init__(original_training_data=training_data,
                                         training_data=training_data.copy(),
                                         R=R,
                                         num_features=num_features,
                                         **prioritize_dicts(self._HARD_CODED_INPUTS, kwargs))

        if training_data.shape != R.shape:
            raise InputError("Training data and R (Binary-valued indicator matrix) should have the same shape.")

        self.m, self.n = self.training_data.shape
        self.theta, self.features = None, None

        # Initialize Variables
        self._j_cost_history = np.array([])
        self._cur_iteration = 0

        self._mu = r2c(np.zeros(self.m) + ((np.max(self.training_data[self.R == 1])
                                            + np.min(self.training_data[self.R == 1])) / 2))

        self._mean_normalization()

    def _mean_normalization(self):
        for i in range(self.m):  # for each product
            ratings = self.training_data[i][self.R[i] == 1]
            self._mu[i][0] = np.mean(ratings)

        self.training_data = self.training_data - self._mu

    @classmethod
    def _hypothesis(cls, X, theta):
        return X @ theta.T

    def cost_and_gradient(self, features_theta_rolled, training_data, R, regularization=True,
                     regularization_lambda=Continuous.REGULARIZATION_LAMBDA):
        """
        Should return the cost and gradient of a certain features/theta prediction

        :param features_theta_rolled: a 1-D array of features and theta arrays
                                        features: newly learned/created features
                                        theta: specific prediction to check
        :type features_theta_rolled: numpy array
        :param training_data: Dataset to train algorithm to - The information you know, for the
        :type training_data: 2-D numpy array
        :param R: Binary-valued indicator matrix,
                   where R[i][j] = 1 if Y[i][j] is given, and R[i][j] = 0 otherwise.
        :type R: 2-D numpy array
        :param regularization: if cost should use a regularization term to regularize thetas (except for theta zero)
        :type regularization: bool
        :param regularization_lambda: The size of lambda for the regularization term
                                        By default - is 1.
        :type regularization_lambda: int or float

        :return: the cost of the prediction, and the gradient in which to change self.features and self.theta.
        :rtype: tuple of float, array
        """
        features, theta = self._unroll(features_theta_rolled)

        hypothesis = self._hypothesis(features, theta)
        predictions_exist = hypothesis * R
        y_exist = training_data * R

        difference = predictions_exist - y_exist

        cost_vector = difference ** 2
        features_gradient = difference @ theta
        theta_gradient = difference.T @ features

        if regularization:
            regularization_features_cost = regularization_lambda * np.sum(features ** 2)
            regularization_theta_cost = regularization_lambda * np.sum(theta ** 2)
            cost_regularization = regularization_features_cost + regularization_theta_cost

            regularization_features_gradient = regularization_lambda * features
            regularization_theta_gradient = regularization_lambda * theta
        else:
            cost_regularization = 0
            regularization_features_gradient = 0
            regularization_theta_gradient = 0

        j_cost = (np.sum(cost_vector) + cost_regularization) / 2
        gradient = np.append(features_gradient + regularization_features_gradient,
                             theta_gradient + regularization_theta_gradient)

        return j_cost, gradient

    def compute_cost(self, features_theta_rolled, training_data, R, regularization=True,
                     regularization_lambda=Continuous.REGULARIZATION_LAMBDA):
        """
        Should return the cost of a certain features/theta prediction

        :param features_theta_rolled: a 1-D array of features and theta arrays
                                        features: newly learned/created features
                                        theta: specific prediction to check
        :type features_theta_rolled: numpy array
        :param training_data: Dataset to train algorithm to - The information you know, for the
        :type training_data: 2-D numpy array
        :param R: Binary-valued indicator matrix,
                   where R[i][j] = 1 if Y[i][j] is given, and R[i][j] = 0 otherwise.
        :type R: 2-D numpy array
        :param regularization: if cost should use a regularization term to regularize thetas (except for theta zero)
        :type regularization: bool
        :param regularization_lambda: The size of lambda for the regularization term
                                        By default - is 1.
        :type regularization_lambda: int or float

        :return: the cost of the prediction
        :rtype: float
        """
        return self.cost_and_gradient(features_theta_rolled, training_data, R, regularization=regularization,
                                      regularization_lambda=regularization_lambda)[0]

    def get_gradient(self, features_theta_rolled, training_data, R, regularization=True,
                     regularization_lambda=Continuous.REGULARIZATION_LAMBDA):
        """
        This method checks the gradient in which to change self.features and self.theta.

        :param features_theta_rolled: a 1-D array of features and theta arrays
                                        features: newly learned/created features
                                        theta: specific prediction to check
        :type features_theta_rolled: numpy array
        :param training_data: Dataset to train algorithm to - The information you know, for the
        :type training_data: 2-D numpy array
        :param R: Binary-valued indicator matrix,
                   where R[i][j] = 1 if Y[i][j] is given, and R[i][j] = 0 otherwise.
        :type R: 2-D numpy array
        :param regularization: if gradient should use a regularization term to regularize thetas (except for theta zero)
        :type regularization: bool
        :param regularization_lambda: The size of lambda for the regularization term
                                        By default - is 1.
        :type regularization_lambda: int or float

        :return: gradient for all features and thetas (rolled into a single numpy array)
        :rtype: numpy array
        """
        return self.cost_and_gradient(features_theta_rolled, training_data, R, regularization=regularization,
                                      regularization_lambda=regularization_lambda)[1]

    def _final_print(self):
        if self.verbose:
            cost = self._j_cost_history[-1]
            error = self.get_error(self.original_training_data, self.R, self.theta, self.features)
            print(f'Final Training Values:    Error - {round(error, 4)} ; Cost - {round(cost, 4)}')

    def _run_gradient_descent_optimized(self):
        import scipy.optimize as spopt

        kwargs = dict(
            training_data=self.training_data,
            R=self.R,
            regularization=self.regularization,
            regularization_lambda=self.regularization_lambda
        )

        result = spopt.minimize(partial(self.cost_and_gradient, **kwargs),
                                self._roll(self.features, self.theta),
                                method=self.optimization_method,
                                jac=True,
                                callback=self._theta_minimizer_callback_func,
                                options=dict(maxiter=self.iterations, disp=self.optimizer_verbose))

        if not result.success:
            self._manage_optimization_error(result.message)

        self.features, self.theta = self._unroll(result.x)
        self._add_cost()

    def _theta_minimizer_callback_func(self, cur_features_theta_rolled):
        self._cur_iteration += 1
        self._add_cost(cur_features_theta_rolled)

    def _add_cost(self, cur_features_theta_rolled=None):
        if cur_features_theta_rolled is None:
            cur_features_theta_rolled = self._roll(self.features, self.theta)
        cost = self.compute_cost(cur_features_theta_rolled, self.training_data, self.R, self.regularization,
                                 regularization_lambda=self.regularization_lambda)
        self._j_cost_history = np.append(self._j_cost_history, cost)

    def _initialize_all_data(self):
        self._initialize_theta()
        self._initialize_features()

    def _initialize_theta(self):
        self.theta = np.random.randn(self.n, self.num_features)

    def _initialize_features(self):
        self.features = np.random.randn(self.m, self.num_features)

    def predict(self, product_index, user_index):
        """
        Predict an output (or column of outputs) for a given input (or set of input arrays)

        :param product_index: index of product from rows of training_data
        :type product_index: int
        :param user_index: index of user to predict for
        :type user_index: int

        :return: prediction
        :rtype: float
        """
        return (self.theta[user_index].T @ self.features[product_index]) + self._mu[product_index]

    def full_prediction(self):
        """
        Returns the full matrix of predictions for all users and all products.

        :return: Full prediction matrix
        :rtype: 2-D numpy array of floats
        """
        return self._hypothesis(self.features, self.theta) + self._mu

    def get_error(self, data=None, R=None, theta=None, features=None):
        """
        Should compute and return the error of the current self.theta hypothesis

        :param data: test info
        :type data: 2-D array
        :param R: Binary-valued indicator matrix,
                   where R[i][j] = 1 if data[i][j] is given, and R[i][j] = 0 otherwise.
        :type R: 2-D array
        :param theta: If you wish for a theta different than the current self.theta, you can give it here
        :param features: If you wish for features different than the current self.features, you can give it here
        """
        if theta is None or features is None:
            theta = self.theta
            features = self.features
        if data is None or R is None:
            data = self.training_data
            R = self.R
        if not (data.shape == R.shape == self.training_data.shape == self.R.shape):
            raise InputError("data and R should should the same shape as training_data.")

        return self.compute_cost(self._roll(features, theta), data - self._mu, R, regularization=False)

    def plot_2feature_hypothesis(self, **kwargs):
        raise NotImplementedError()

    def plot_1feature_hypothesis(self, **kwargs):
        raise NotImplementedError()

    def _unroll(self, array):
        features = array[:self.m * self.num_features].reshape(self.m, self.num_features)
        theta = array[self.m * self.num_features:].reshape(self.n, self.num_features)
        return features, theta

    @staticmethod
    def _roll(features, theta):
        return np.append(features, theta)
