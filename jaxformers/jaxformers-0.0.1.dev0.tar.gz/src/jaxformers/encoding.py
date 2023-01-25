import jax
from flax import linen as nn
from jax import numpy as jnp


class PositionalEncoding(nn.Module):
    embed_dim: int = 512
    max_seq_len: int = 512

    def setup(self) -> None:
        self.positional_encoding = jnp.zeros((1, self.max_seq_len, self.embed_dim))
        x = jnp.arange(self.max_seq_len, dtype=jnp.float32).reshape(-1, 1) / jnp.power(
            10000, jnp.arange(0, self.embed_dim, 2, dtype=jnp.float32) / self.embed_dim
        )
        self.positional_encoding = self.positional_encoding.at[:, :, 0::2].set(
            jnp.sin(x)
        )
        self.positional_encoding = self.positional_encoding.at[:, :, 1::2].set(
            jnp.cos(x)
        )

    @nn.compact
    def __call__(self, x: jax.Array) -> jax.Array:
        assert x.ndim == 3, "x must be of shape [batch_size, seq_len, embed_dim]"
        assert x.dtype in [
            jnp.float16,
            jnp.float32,
            jnp.float64,
        ], "x must be of dtype float (float16, float32, float64)"
        return x + self.positional_encoding[:, : x.shape[1], :]
