import numpy as np
import pytest
import torch
from dnn_cool_activations.base import softmax
from torch.nn import functional as F

from dnn_cool_losses.base import (
    cross_entropy_on_logits,
    cross_entropy_on_proba,
    binary_cross_entropy_on_logits,
    absolute_error,
    squared_error,
)


def test_cross_entropy_on_logits():
    logits = np.array([[0.0, 1e5, 0.0], [1e4, 0.0, 0.0]])
    targets = np.array([1, 0])
    assert cross_entropy_on_logits(logits, targets, axis=1).mean() < 1e-5


def test_cross_entropy_on_proba():
    proba = np.array([[0.0, 1.0, 0.0], [1.0, 0.0, 0.0]])
    targets = [1, 0]
    assert cross_entropy_on_proba(proba, targets, axis=1).mean() < 1e-5


@pytest.mark.parametrize("seed", list(range(20)))
def test_logits_proba_rel(seed):
    np.random.seed(seed)
    logits = np.random.randn(16, 3)
    targets = logits.argmax(axis=1)
    per_sample_logits = cross_entropy_on_logits(logits, targets, axis=1)
    probas = softmax(logits, axis=1)
    per_sample_proba = cross_entropy_on_proba(probas, targets, axis=-1)
    assert np.allclose(per_sample_logits, per_sample_proba)

    logits_t = torch.tensor(logits)
    targets_t = torch.tensor(targets)
    pytorch_res = F.cross_entropy(logits_t, targets_t, reduction="none").numpy()
    assert np.allclose(pytorch_res, per_sample_proba)


@pytest.mark.parametrize("seed", list(range(20)))
def test_binary_cross_entropy(seed):
    np.random.seed(seed)
    logits = np.random.randn(16, 1)
    targets = (logits > 0.5).astype(float)
    per_sample_logits = binary_cross_entropy_on_logits(logits, targets)

    logits_t = torch.tensor(logits)
    targets_t = torch.tensor(targets)
    pytorch_res = F.binary_cross_entropy_with_logits(logits_t, targets_t, reduction="none")

    assert np.allclose(per_sample_logits, pytorch_res)


@pytest.mark.parametrize("seed", list(range(20)))
def test_absolute_error(seed):
    np.random.seed(seed)
    logits = np.random.randn(16, 1)
    targets = np.floor(logits)
    per_sample = absolute_error(logits, targets)

    logits_t = torch.tensor(logits)
    targets_t = torch.tensor(targets)
    pytorch_res = F.l1_loss(logits_t, targets_t, reduction="none")

    assert np.allclose(per_sample, pytorch_res)


@pytest.mark.parametrize("seed", list(range(20)))
def test_squared_error(seed):
    np.random.seed(seed)
    logits = np.random.randn(16, 1)
    targets = np.floor(logits)
    per_sample = squared_error(logits, targets)

    logits_t = torch.tensor(logits)
    targets_t = torch.tensor(targets)
    pytorch_res = F.mse_loss(logits_t, targets_t, reduction="none")

    assert np.allclose(per_sample, pytorch_res)
