import tensorwrap as tf
import jax
from tensorwrap.module import Module


class Optimizer(Module):

    def __init__(self, lr=0.01):
        self.lr = lr


class SGD(Optimizer):
    def __init__(self, learning_rate=0.01):
        super().__init__(lr=learning_rate)

    def apply_gradients(self, gradients, layers):
        for layer in layers:
            kernel = layer.trainable_variables[0]
            bias = layer.trainable_variables[1]
            layer.trainable_variables[0] = jax.tree_map(lambda x: x + gradients * self.lr, kernel)
            layer.trainable_variables[1] = jax.tree_map(lambda x: x + gradients * self.lr, bias)
        return layers
