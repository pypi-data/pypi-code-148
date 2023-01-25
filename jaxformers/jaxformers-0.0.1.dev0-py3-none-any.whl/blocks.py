from typing import Union

import jax
from flax import linen as nn
from jax import numpy as jnp

from jaxformers.attention import MultiHeadAttention
from jaxformers.normalization import LayerNorm


class MLPBlock(nn.Module):
    in_features: int = 2048
    dropout_rate: float = 0.1

    @nn.compact
    def __call__(self, x: jax.Array, training: bool = False) -> jax.Array:
        assert x.ndim == 3, "x must be of shape [batch_size, seq_len, embed_dim]"
        assert x.dtype in [
            jnp.float16,
            jnp.float32,
            jnp.float64,
        ], "x must be of dtype float (float16, float32, float64)"
        out_features = x.shape[-1]

        x = nn.Dense(features=self.in_features)(x)
        x = nn.relu(x)
        x = nn.Dropout(rate=self.dropout_rate)(x, deterministic=not training)
        x = nn.Dense(features=out_features)(x)
        x = nn.Dropout(rate=self.dropout_rate)(x, deterministic=not training)
        return x


class EncoderBlock(nn.Module):
    embed_dim: int = 512
    num_heads: int = 8
    mlp_in_features: int = 2048
    dropout_rate: float = 0.1

    @nn.compact
    def __call__(self, x: jax.Array, training: bool = False) -> jax.Array:
        assert x.ndim == 3, "x must be of shape [batch_size, seq_len, embed_dim]"
        assert x.dtype in [
            jnp.float16,
            jnp.float32,
            jnp.float64,
        ], "x must be of dtype float (float16, float32, float64)"

        attention_out = MultiHeadAttention(
            num_heads=self.num_heads, embed_dim=self.embed_dim
        )(k=x, v=x, q=x)
        x += nn.Dropout(rate=self.dropout_rate)(
            attention_out, deterministic=not training
        )
        x = LayerNorm()(x)

        mlp_out = MLPBlock(in_features=self.mlp_in_features)(x)
        x += nn.Dropout(rate=self.dropout_rate)(mlp_out, deterministic=not training)
        return LayerNorm()(x)


class DecoderBlock(nn.Module):
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

        attention_out = MultiHeadAttention(
            num_heads=self.num_heads, embed_dim=self.embed_dim
        )(k=x, v=x, q=x, mask=mask)
        x += nn.Dropout(rate=self.dropout_rate)(
            attention_out, deterministic=not training
        )
        x = LayerNorm()(x)

        attention_out = MultiHeadAttention(
            num_heads=self.num_heads, embed_dim=self.embed_dim
        )(k=memory_k, v=memory_v, q=x, mask=mask)
        x += nn.Dropout(rate=self.dropout_rate)(
            attention_out, deterministic=not training
        )
        x = LayerNorm()(x)

        mlp_out = MLPBlock(in_features=self.mlp_in_features)(x)
        x += nn.Dropout(rate=self.dropout_rate)(mlp_out, deterministic=not training)
        return LayerNorm()(x)
