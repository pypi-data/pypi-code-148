import jax.random
from functools import partial
from jax import jit
from jaxtyping import Array
from tensorwrap.module import Module
import tensorwrap as tf
import jax.numpy as jnp
from random import randint


class Layer(Module):
    """A base layer class that is used to create new JIT enabled layers.
       Acts as the subclass for all layers, to ensure that they are converted in PyTrees."""

    def __init__(self, trainable=True, dtype=None, **kwargs) -> None:
        self.trainable = trainable
        self.dtype = dtype
        self.kwargs = kwargs

    @classmethod
    def add_weights(self, shape=None, initializer='glorot_uniform', trainable=True, name=None):
        """Useful method inherited from layers.Layer that adds weights that can be trained.
        Arguments:
            - shape: Shape of the inputs and the units
            - initializer: The initial values of the weights
            - trainable - Not required or implemented yet."""

        if initializer == 'zeros':
            return jnp.zeros(shape, dtype=jnp.float32)

        elif initializer == 'glorot_normal':
            key = jax.random.PRNGKey(randint(1, 10))
            return jax.random.normal(key, shape, dtype = tf.float32)

        elif initializer == 'glorot_uniform':
            key = jax.random.PRNGKey(randint(1, 5))
            return jax.random.uniform(key, shape, dtype = tf.float32)

    def build(self, input_shape):
        input_dims = len(input_shape)
        if input_dims <= 1:
            raise ValueError("Input to the Dense layer has dimensions less than 1."
                             "Use tf.expand_dims or tf.reshape(-1, 1) in order to expand dimensions.")
        self.built = True
        self.trainable_variables = [self.kernel, self.bias]

    def call(self) -> None:
        # Must be defined to satisfy arbitrary method.
        pass
    

    def __call__(self, inputs):
        # This will be called when called normally.
        if not self.built:
            self.build(inputs.shape)
        out = self.call(inputs)
        return out


class Linear(Layer):
    def __init__(self,
                 units,
                 activation=None,
                 use_bias=True,
                 kernel_initializer='glorot_uniform',
                 bias_initializer='zeros',
                 kernel_regularizer=None,
                 bias_regularizer=None,
                 activity_regularizer=None,
                 kernel_constraint=None,
                 bias_constraint=None,
                 *args,
                 **kwargs):
        super(Module, self).__init__(units=units,
                                     activation=activation,
                                     use_bias=use_bias,
                                     kernel_initializer=kernel_initializer,
                                     bias_initializer=bias_initializer,
                                     kernel_regularizer=kernel_regularizer,
                                     bias_regularizer=bias_regularizer,
                                     activity_regularizer=activity_regularizer,
                                     kernel_constraint=kernel_constraint,
                                     bias_constraint=bias_constraint,
                                     built=False,
                                     dynamic=not tf.test.is_device_available())

    def build(self, input_shape):
        self.kernel = self.add_weights(shape=(input_shape[-1], self.units),
                                       initializer=self.kernel_initializer,
                                       name="kernel")
        self.bias = self.add_weights(shape=(self.units),
                                     initializer=self.bias_initializer,
                                     name="bias")
        super().build(input_shape)

    def call(self, inputs: Array) -> Array:
        self.built = False
        if self.use_bias == True:
            return jnp.matmul(inputs, self.trainable_variables[0]) + self.trainable_variables[1]
        else:
            return jnp.matmul(inputs, self.trainable_variables[0])
