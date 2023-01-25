from typing import Union

import flax.linen as nn
import jax
from jax import numpy as jnp

from jaxformers.blocks import DecoderBlock


class Decoder(nn.Module):
    num_layers: int = 12
    embed_dim: int = 512
    num_heads: int = 8
    mlp_in_features: int = 2048
    dropout_rate: float = 0.1

    @nn.compact
    def __call__(
        self,
        x: jax.Array,
        memory_k: jax.Array,
        memory_v: jax.Array,
        mask: Union[jax.Array, None] = None,
        training: bool = False,
    ) -> jax.Array:
        assert x.ndim == 3, "x must be of shape [batch_size, seq_len, embed_dim]"
        assert x.dtype in [
            jnp.float16,
            jnp.float32,
            jnp.float64,
        ], "x must be of dtype float (float16, float32, float64)"
        assert (
            memory_k.ndim == 3
        ), "memory_k must be of shape [batch_size, seq_len, embed_dim]"
        assert memory_k.dtype in [
            jnp.float16,
            jnp.float32,
            jnp.float64,
        ], "memory_k must be of dtype float (float16, float32, float64)"
        assert (
            memory_v.ndim == 3
        ), "memory_v must be of shape [batch_size, seq_len, embed_dim]"
        assert memory_v.dtype in [
            jnp.float16,
            jnp.float32,
            jnp.float64,
        ], "memory_v must be of dtype float (float16, float32, float64)"
        for _ in range(self.num_layers):
            x = DecoderBlock(
                embed_dim=self.embed_dim,
                num_heads=self.num_heads,
                mlp_in_features=self.mlp_in_features,
                dropout_rate=self.dropout_rate,
            )(x=x, memory_k=memory_k, memory_v=memory_v, mask=mask, training=training)
        return x
