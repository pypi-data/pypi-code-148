""" TensorWrap's initial API. This API contains various frontend functions that are
used to manipulate tensors and various data. However, most of the API currently borrows
from JAX's built-in operations. For neural networks, please use the Keras API or import
the Torch API to use PyTorch variants."""

# Error Silencer:
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

# Library Paths:
from tensorwrap import nn
from tensorwrap import module
from tensorwrap import test
from tensorwrap import config

# Path Shortener:
from tensorwrap.module import Module
from tensorwrap.version import __version__
from tensorwrap.experimental.wrappers import function

# JAX Built-ins:
from jax.numpy import array as Variable
from jax.numpy import float16, float32, float64
from jax.numpy import int16, int32, int64
from jax.numpy import matmul, square, abs, mean
from jax.numpy import reshape