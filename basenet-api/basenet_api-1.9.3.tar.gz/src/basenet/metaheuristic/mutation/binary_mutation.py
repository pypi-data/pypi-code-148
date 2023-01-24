# - x - x - x - x - x - x - x - x - x - x - x - x - x - x - #
#                                                           #
#   This file was created by: Alberto Palomo Alonso         #
# Universidad de Alcalá - Escuela Politécnica Superior      #
#                                                           #
# - x - x - x - x - x - x - x - x - x - x - x - x - x - x - #
# Import statements:
import tensorflow as tf
import numpy as np


# -----------------------------------------------------------
def binary_mutation(population: tf.Tensor, mutation_rate: float = 0.2) -> tf.Tensor:
    """
    This mutation works with binary individuals. It swaps 0 to 1 with a mutation rate.
    :param population: The current individuals.
    :param mutation_rate: The probability that a parameter toss.
    :return: The new individuals with the mutation.
    """
    new_indis = list()
    for individual in population.numpy():
        this_indi = list()
        for parameter in individual:
            mutation = np.random.choice(2, p=[1 - mutation_rate, mutation_rate])
            if mutation and parameter == 0:
                this_indi.append(1)
            elif mutation and parameter == 1:
                this_indi.append(0)
            else:
                this_indi.append(parameter)
        new_indis.append(this_indi)
    return tf.convert_to_tensor(new_indis, dtype=tf.float32)
# - x - x - x - x - x - x - x - x - x - x - x - x - x - x - #
#                        END OF FILE                        #
# - x - x - x - x - x - x - x - x - x - x - x - x - x - x - #
