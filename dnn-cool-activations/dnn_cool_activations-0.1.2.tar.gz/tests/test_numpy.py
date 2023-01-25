import numpy as np
import pytest
import torch
from torch.nn import functional as F

from dnn_cool_activations.base import sigmoid, softmax


@pytest.mark.parametrize("seed", list(range(20)))
def test_sigmoid(seed):
    np.random.seed(seed)
    logits = np.random.randn(16, 3)
    activation_np = sigmoid(logits)
    actions_torch = torch.sigmoid(torch.tensor(logits)).numpy()
    assert np.allclose(activation_np, actions_torch)


@pytest.mark.parametrize("seed", list(range(20)))
def test_softmax(seed):
    np.random.seed(seed)
    logits = np.random.randn(16, 3)
    activation_np = softmax(logits, axis=1)
    actions_torch = torch.softmax(torch.tensor(logits), dim=1).numpy()
    assert np.allclose(activation_np, actions_torch)

