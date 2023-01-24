# - x - x - x - x - x - x - x - x - x - x - x - x - x - x - #
#                                                           #
#   This file was created by: Alberto Palomo Alonso         #
# Universidad de Alcalá - Escuela Politécnica Superior      #
#                                                           #
# - x - x - x - x - x - x - x - x - x - x - x - x - x - x - #
# Import statements:
from abc import ABC
import tensorflow as tf
from ..basis import BaseNetHeuristic, HeuristicConstraints
from ..crossover import uniform_crossover
from ..initialization import random_initializer
from ..selection import elitist_selection
from ..mutation import gaussian_mutation
from .._utils.utils import get_algorithm_parameters
# -----------------------------------------------------------


class BaseNetGenetic(BaseNetHeuristic, ABC):
    def __init__(self, *args, **kwargs):
        """
        The BaseNetGenetic algorithm includes genetic algorithm with the following configuration:
            initializer: random_initializer
            crossover: uniform_crossover
            mutation: gaussian_mutation
            selection: elitist_selection
        :param args: Must include the fitness function as first parameter.
        :param kwargs: Contains the genetic algorithm parameters:
            :param mask: A crossover mask if given.
            :param crossover_rate: The probability that a parameter is chosen for crossover for random mask.
            :param mutation_variance: The variance of the gaussian in the mutation function.
        """
        self.mask, self.crossover_rate, self.mutation_variance, kwargs =\
            get_algorithm_parameters(mask=None,
                                     crossover_rate=0.5,
                                     mutation_variance='must',
                                     kwargs=kwargs)
        super().__init__(*args, **kwargs)

    @staticmethod
    def initializer(number_of_individuals: int, constraints: HeuristicConstraints) -> tf.Tensor:
        return random_initializer(number_of_individuals, constraints)

    def crossover(self, number_of_new_individuals: int, population: tf.Tensor) -> tf.Tensor:
        non_muted = uniform_crossover(number_of_new_individuals, population, self.mask, self.crossover_rate)
        muted = gaussian_mutation(non_muted, self.mutation_variance)
        return muted

    @staticmethod
    def selection(new_individuals: tf.Tensor, population: tf.Tensor) -> tf.Tensor:
        return elitist_selection(new_individuals, population)
# - x - x - x - x - x - x - x - x - x - x - x - x - x - x - #
#                        END OF FILE                        #
# - x - x - x - x - x - x - x - x - x - x - x - x - x - x - #
