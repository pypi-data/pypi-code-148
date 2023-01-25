import jax
from flax import linen as nn
from jax import numpy as jnp


class LayerNorm(nn.Module):
    eps: float = 1e-5

    @nn.compact
    def __call__(self, x: jax.Array) -> jax.Array:
        assert x.ndim > 1, "x must be of shape [batch_size, ...]"
        gamma = self.param("scale", nn.initializers.ones, x.shape[1:])
        beta = self.param("bias", nn.initializers.zeros, x.shape[1:])
        mean = jnp.mean(x, axis=-1, keepdims=True)
        std = jnp.std(x, axis=-1, keepdims=True)
        return jnp.asarray((gamma * (x - mean) / jnp.sqrt(std + self.eps)) + beta)
