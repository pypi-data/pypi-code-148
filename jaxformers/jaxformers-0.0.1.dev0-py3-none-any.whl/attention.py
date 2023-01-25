from typing import Tuple, Union

import jax
from flax import linen as nn
from jax import numpy as jnp


class SelfAttention(nn.Module):
    embed_dim: int = 512

    @nn.compact
    def __call__(
        self, k: jax.Array, v: jax.Array, q: jax.Array, return_attention: bool = False
    ) -> Union[jax.Array, Tuple[jax.Array, jax.Array]]:
        assert k.ndim == 3, "k must be of shape [batch_size, seq_len, embed_dim]"
        assert k.dtype in [
            jnp.float16,
            jnp.float32,
            jnp.float64,
        ], "k must be of dtype float (float16, float32, float64)"
        assert v.ndim == 3, "v must be of shape [batch_size, seq_len, embed_dim]"
        assert v.dtype in [
            jnp.float16,
            jnp.float32,
            jnp.float64,
        ], "v must be of dtype float (float16, float32, float64)"
        assert q.ndim == 3, "q must be of shape [batch_size, seq_len, embed_dim]"
        assert q.dtype in [
            jnp.float16,
            jnp.float32,
            jnp.float64,
        ], "q must be of dtype float (float16, float32, float64)"
        assert k.shape == v.shape, "k and v must have the same shape"
        assert k.shape == q.shape, "k and q must have the same shape"

        k_proj = nn.Dense(features=self.embed_dim)(k)
        v_proj = nn.Dense(features=self.embed_dim)(v)
        q_proj = nn.Dense(features=self.embed_dim)(q)

        energy = jnp.einsum("bqd,bkd->bqk", q_proj, k_proj)
        attention = nn.softmax(energy / jnp.sqrt(self.embed_dim), axis=-1)
        out = jnp.einsum("bqk,bkd->bqd", attention, v_proj)
        linear_out = nn.Dense(features=self.embed_dim)(out)
        if return_attention:
            return linear_out, attention
        return linear_out


class MultiHeadAttention(nn.Module):
    num_heads: int = 8
    embed_dim: int = 512
    head_dim: int = embed_dim // num_heads

    def setup(self) -> None:
        assert (self.head_dim * self.num_heads) == self.embed_dim, (
            "embed_dim must be equal to num_heads * head_dim, this means that embed_dim"
            " must be integer divisible by num_heads."
        )

    @nn.compact
    def __call__(
        self,
        k: jax.Array,
        v: jax.Array,
        q: jax.Array,
        mask: Union[jax.Array, None] = None,
        return_attention: bool = False,
    ) -> Union[jax.Array, Tuple[jax.Array, jax.Array]]:
        assert k.ndim == 3, "k must be of shape [batch_size, seq_len, embed_dim]"
        assert k.dtype in [
            jnp.float16,
            jnp.float32,
            jnp.float64,
        ], "k must be of dtype float (float16, float32, float64)"
        assert v.ndim == 3, "v must be of shape [batch_size, seq_len, embed_dim]"
        assert v.dtype in [
            jnp.float16,
            jnp.float32,
            jnp.float64,
        ], "v must be of dtype float (float16, float32, float64)"
        assert q.ndim == 3, "q must be of shape [batch_size, seq_len, embed_dim]"
        assert q.dtype in [
            jnp.float16,
            jnp.float32,
            jnp.float64,
        ], "q must be of dtype float (float16, float32, float64)"
        assert k.shape == v.shape, "k and v must have the same shape"
        assert k.shape == q.shape, "k and q must have the same shape"
        assert (
            mask is None or mask.ndim == 2
        ), "mask must be of shape [batch_size, seq_len]"

        batch_size, seq_len = q.shape[0], q.shape[1]

        k_proj = nn.Dense(features=self.embed_dim)(k)
        k_proj = k_proj.reshape((batch_size, self.num_heads, seq_len, self.head_dim))

        v_proj = nn.Dense(features=self.embed_dim)(v)
        v_proj = v_proj.reshape((batch_size, self.num_heads, seq_len, self.head_dim))

        q_proj = nn.Dense(features=self.embed_dim)(q)
        q_proj = q_proj.reshape((batch_size, self.num_heads, seq_len, self.head_dim))

        energy = jnp.einsum("bhqd,bhkd->bhqk", q_proj, k_proj)
        energy /= jnp.sqrt(self.embed_dim)
        if mask is not None:
            energy = jnp.where(mask == 0, -1e9, energy)
        attention = nn.softmax(energy, axis=-1)
        out = jnp.einsum("bhqk,bhkd->bhqd", attention, v_proj)
        out = out.reshape((batch_size, seq_len, self.embed_dim))
        linear_out = nn.Dense(features=self.embed_dim)(out)
        if return_attention:
            return linear_out, attention
        return linear_out
