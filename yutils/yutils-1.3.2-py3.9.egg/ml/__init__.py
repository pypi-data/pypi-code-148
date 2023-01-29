#!%PYTHON_HOME%\python.exe
# coding: utf-8
# version: python38

from yutils.ml.data.data_sets import DataSets, create_data_sets_object_from_precreated_sets, SimpleDataSet
from yutils.ml.data.features import FeatureNormalizer, AddPolynomialFeatures
from yutils.ml.data.pca import PCA
from yutils.ml.base.ml_base import create_data_from_text_file, add_ones
from yutils.ml.impl.plotting.curves import plot_learning_curve, plot_validation_curve, print_strategy

# Supervised Learning
from yutils.ml.models.supervised.ml_optimizer import MLOptimizer
# Import Models
from yutils.ml.models.supervised.others.continuous.normal_equation import NormalEquation
from yutils.ml.models.supervised.regression.classification.logistic_regression import LogisticRegression
from yutils.ml.models.supervised.regression.classification.multiclass_classification import MultiClassClassification
from yutils.ml.models.supervised.regression.classification.neural_network import NeuralNetwork
from yutils.ml.models.supervised.regression.classification.svm import SVM
from yutils.ml.models.supervised.regression.continuous.collaborative_filtering import CollaborativeFiltering
from yutils.ml.models.supervised.regression.continuous.linear_regression import LinearRegression

# Unsupervised Learning
from yutils.ml.models.unsupervised.clustering.k_means import KMeans

# TODO: In Supervised models / DataSets:
#                           add normalization of y if range of y is extremely large, multiple orders of magnitude.
