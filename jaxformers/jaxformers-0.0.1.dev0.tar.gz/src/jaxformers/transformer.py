from typing import Union

import jax
from flax import linen as nn
from jax import numpy as jnp

from jaxformers.decoder import Decoder
from jaxformers.encoder import Encoder
from jaxformers.encoding import PositionalEncoding


class Transformer(nn.Module):
    embed_dim: int = 512
    max_seq_len: int = 512
    encoder_vocab_size: int = 256
    encoder_num_layers: int = 6
    encoder_num_heads: int = 8
    encoder_mlp_in_features: int = 2048
    encoder_dropout_rate: float = 0.1
    decoder_vocab_size: int = 256
    decoder_num_layers: int = 6
    decoder_num_heads: int = 8
    decoder_mlp_in_features: int = 2048
    decoder_dropout_rate: float = 0.1
    training: bool = False

    @nn.compact
    def __call__(
        self, x_in: jax.Array, x_out: jax.Array, mask_out: Union[jax.Array, None] = None
    ) -> jax.Array:
        assert x_in.ndim == 2, "x_in must be of shape [batch_size, seq_len]"
        assert x_in.dtype in [
            jnp.int8,
            jnp.int16,
            jnp.int32,
            jnp.int64,
        ], "x_in must be of dtype int (int8, int16, int32, int64)"
        assert x_out.ndim == 2, "x_out must be of shape [batch_size, seq_len]"
        assert x_in.dtype in [
            jnp.int8,
            jnp.int16,
            jnp.int32,
            jnp.int64,
        ], "x_out must be of dtype int (int8, int16, int32, int64)"

        x_in = nn.Embed(
            num_embeddings=self.encoder_vocab_size, features=self.embed_dim
        )(x_in)
        x_in = PositionalEncoding(
            embed_dim=self.embed_dim, max_seq_len=self.max_seq_len
        )(x_in)

        x_mem = Encoder(
            num_layers=self.encoder_num_layers,
            embed_dim=self.embed_dim,
            num_heads=self.encoder_num_heads,
            mlp_in_features=self.encoder_mlp_in_features,
            dropout_rate=self.encoder_dropout_rate,
        )(x=x_in, training=self.training)

        x_out = nn.Embed(
            num_embeddings=self.decoder_vocab_size, features=self.embed_dim
        )(x_out)
        x_out = PositionalEncoding(
            embed_dim=self.embed_dim, max_seq_len=self.max_seq_len
        )(x_out)

        out = Decoder(
            num_layers=self.decoder_num_layers,
            embed_dim=self.embed_dim,
            num_heads=self.decoder_num_heads,
            mlp_in_features=self.decoder_mlp_in_features,
            dropout_rate=self.decoder_dropout_rate,
        )(
            x=x_out,
            memory_k=x_mem,
            memory_v=x_mem,
            mask=mask_out,
            training=self.training,
        )

        out = nn.Dense(features=self.embed_dim)(out)
        return nn.softmax(out, axis=-1)
