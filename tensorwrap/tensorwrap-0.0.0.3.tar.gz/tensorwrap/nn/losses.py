from tensorwrap.module import Module
import tensorwrap as tf
from jax import jit

class Loss(Module):
    """A base loss class that is used to create new loss functions.
       Acts as a subclass for all losses, to ensure that it is compatible with PyTrees and XLA."""
    def __init__(self, dynamic=False):
        self.dynamic = dynamic

    def __call__(self):
        if not self.dynamic:
            call = jit(self.call)
        else:
            call = self.call
        return call()

    def call(self):
        pass

# class MSE(Loss):
#     """ Computes the mean square loss, once given the true and pred values."""
#
#     def __init__(self, y_true, y_pred):
#         self.y_pred = y_pred
#         self.y_true = y_true
#
#     def call(self):
#         return tf.square(tf.mean(self.y_pred - self.y_true))
#
# class MAE(Loss):
#     """ Computes the mean square loss, once given the true and pred values."""
#
#     def __init__(self, y_true, y_pred):
#         self.y_pred = y_pred
#         self.y_true = y_true
#
#     def call(self):
#         return tf.abs(tf.mean(self.y_pred - self.y_true))


def mse(y_true, y_pred):
    return tf.square(y_pred - y_true)


def mae(y_true, y_pred):
    return tf.mean(tf.abs(y_pred - y_true))
