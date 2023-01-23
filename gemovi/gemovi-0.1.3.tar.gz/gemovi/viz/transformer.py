from __future__ import annotations

import functools

import numpy as np
import torch

from gemovi.common.constants import get_device
from gemovi.common.utils import tensor_to_np

device = get_device(1)


def _ensure_tensor(array):
    if isinstance(array, np.ndarray):
        return torch.from_numpy(array).to(device)
    return array


def allow_none_func_and_tensor_data(func, X, **kwargs) -> torch.Tensor:
    if func is None:
        return _ensure_tensor(X)
    if isinstance(X, torch.Tensor):
        X = tensor_to_np(X)
    out_kwargs = {}
    for k, v in kwargs.items():
        if isinstance(v, torch.Tensor):
            v = tensor_to_np(v)
        out_kwargs[k] = v

    out = func(X, **out_kwargs)
    return _ensure_tensor(out)


def _xycallable(
    X: torch.Tensor | np.ndarray, *, y: torch.Tensor = None
) -> torch.Tensor:
    ...


def _xcallable(X: torch.Tensor | np.ndarray) -> torch.Tensor:
    ...


def NoneTransformer(*args, **kwargs):
    return None


class NpOrNoneTransformer:
    wrapped_traits = ["transform", "fit", "fit_transform"]
    transform = _xcallable
    fit = _xycallable
    fit_transform = _xycallable

    def __init__(self, transformer=None):
        self.transformer = None
        self.set_transformer(transformer)

    def set_transformer(self, transformer=None):
        self.transformer = transformer
        for trait in self.wrapped_traits:
            to_wrap = getattr(self.transformer, trait, None)
            wrapped = functools.partial(allow_none_func_and_tensor_data, to_wrap)
            setattr(self, trait, wrapped)

    def inverse_transform(self, X: np.ndarray | torch.Tensor) -> torch.Tensor:
        tform_func = getattr(self.transformer, "inverse_transform", None)
        if tform_func is None and self.transformer is not None:
            raise ValueError(
                f"{self.transformer} cannot move from latent space to input space. "
                f"Consider using a different transformer."
            )
        return allow_none_func_and_tensor_data(tform_func, X)

    def implements(self, trait: str) -> bool:
        return self.transformer is None or hasattr(self.transformer, trait)
