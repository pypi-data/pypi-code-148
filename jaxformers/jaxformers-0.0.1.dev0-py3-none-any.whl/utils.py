from typing import Sequence

import jax
from jax import numpy as jnp


def look_ahead_mask(shape: Sequence[int]) -> jax.Array:
    return jnp.triu(jnp.ones(shape), k=1)
