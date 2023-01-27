from typing import Any

import torch.nn as nn

from .rnn_layer import RNNLayer


class LSTM(RNNLayer, nn.LSTM):
    def __init__(self, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)

    def get_output_dim(self) -> int:
        dim: int = self.hidden_size * (int(self.bidirectional) + 1)
        return dim
