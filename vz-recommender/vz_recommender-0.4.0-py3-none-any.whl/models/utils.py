
import math
from typing import *

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch import einsum, nn


class MeanMaxPooling(nn.Module):
    """
    [B, S, E] -> [B, 2*E]
    """
    def __init__(self, axis=1, dropout=0.0):
        super().__init__()
        self.axis = axis
        self.dropout = nn.Dropout(p=dropout)

    def forward(self, inputs, valid_length=None):
        """
        :param inputs: Tensor, shape [batch_size, seq_len, embedding_dim]
        :param valid_length: None or Tensor, valid len of token in the sequence with shape [batch_size]
        :return: Tensor, shape [batch_size, 2 * embedding_dim]
        """
        # TODO: broadcast indexing to mean over first vl
        mean_out = torch.mean(inputs, dim=self.axis) if valid_length is None \
            else torch.sum(inputs, dim=self.axis) / valid_length.add(1E-7).unsqueeze(1)
        max_out = torch.max(inputs, dim=self.axis).values
        outputs = torch.cat((mean_out, max_out), dim=1)
        outputs = self.dropout(outputs)
        return outputs


class Whitening:
    def __init__(self, vecs, n_components=248):
        super().__init__()
        self.vecs = vecs
        self.n_components = n_components
    
    def compute_kernel_bias(self, axis=0, keepdims=True):
        mu = self.vecs.mean(axis=axis, keepdims=keepdims)
        cov = np.cov(self.vecs.T)
        u, s, vh = np.linalg.svd(cov)
        W = np.dot(u, np.diag(1 / np.sqrt(s)))
        return W[:, :self.n_components], -mu

    def transform_and_normalize(self, kernel=None, bias=None):
        if not (kernel is None or bias is None):
            vecs = (self.vecs + bias).dot(kernel)
        return vecs / (self.vecs**2).sum(axis=1, keepdims=True)**0.5
    

class SwiGLU(nn.Module):
    """
    Swish + GLU (SwiGLU) activation function used for Multilayer perceptron(MLP) intermediate activations in transformers.
    classic Noam Shazeer paper, except here they use SwiGLU instead of the more popular GEGLU for gating the feedforward
    https://arxiv.org/abs/2002.05202
    """
    def forward(self, x):
        """
        takes in x input data and returns swiglu

        Args :
            x : input data
        Return : 
                SwiGLU applied activated output
        """
        x, gate = x.chunk(2, dim=-1)
        return F.silu(gate) * x
    

class LayerNorm(nn.Module):
    """
    Applies Layer Normalization for last certain number of dimensions.

    Args :
        dim : Dimension of input
    """
    def __init__(self, dim):
        super().__init__()
        self.gamma = nn.Parameter(torch.ones(dim))
        self.register_buffer("beta", torch.zeros(dim))

    def forward(self, x):
        """
        takes input data x and applies layer normalization

        Args :
            x : input data

        Return :
            The layer normalized values for the input data using gamma and beta init parameters.
        """
        return F.layer_norm(x, x.shape[-1:], self.gamma, self.beta)


class Residual(nn.Module):
    """
    Residual networks

    Args :
        fn : function
    """
    def __init__(self, fn):
        super().__init__()
        self.fn = fn

    def forward(self, x, vl):
        """
        takes in x (input data) ,vl (values) and return residual values

        Args :
            x : input data
            vl : valid length to be used, Tensor, shape [batch_size]

        Return : 
            residual value after applying to a function
        """
        x_out= self.fn(x, vl)
        x_out += x
        return x_out

    
class RotaryEmbedding(nn.Module):
    """
    Rotatory positional (RoPE) embeddings, paper -  https://arxiv.org/abs/2104.09864.
    RoPE encodes the absolute position with a rotation matrix and meanwhile incorporates the explicit relative position dependency in self-attention formulation

    Args :
        dim : dimensions
    """
    def __init__(self, dim):
        super().__init__()
        inv_freq = 1.0 / (10000 ** (torch.arange(0, dim, 2).float() / dim))
        self.register_buffer("inv_freq", inv_freq)

    def forward(self, max_seq_len, *, device):
        """
        takes in max_seq_len, *, device as input and return embeddings

        Args :
            max_seq_len : input data
            * :
            device : device to be used, cpu or gpu

        Return : 
            embeddings
        """
        seq = torch.arange(max_seq_len, device=device, dtype=self.inv_freq.dtype)
        freqs = einsum("i , j -> i j", seq, self.inv_freq)
        return torch.cat((freqs, freqs), dim=-1)
    

class PositionalEncoding(nn.Module):
    """
    PositionalEncoding module injects some information about the relative or absolute position of the tokens in the sequence. 
    The positional encodings have the same dimension as the embeddings so that the two can be summed

    Args :
        d_model: dimension of token embedding
        max_len: max length of sequence
        dropout: dropout field for regularization
    """
    def __init__(self, d_model, max_len=5000, dropout=0.1):
        super().__init__()
        self.dropout = nn.Dropout(p=dropout)

        position = torch.arange(max_len).unsqueeze(1)
        div_term = torch.exp(torch.arange(0, d_model, 2) * (-math.log(10000.0) / d_model))
        pe = torch.zeros(1, max_len, d_model)
        pe[0, :, 0::2] = torch.sin(position * div_term)
        pe[0, :, 1::2] = torch.cos(position * div_term)
        self.register_buffer('pe', pe)

    def forward(self, x):
        """
        Takes in the input value and add the positional value, apply the dropout on top of it and then return the final value.

        Args :
            x: input data

        Return :
            output of positional encoding

        Shape :
            x: [batch_size, seq_len, embedding_dim]
            
            out : [batch_size, seq_len, embedding_dim]

        """
        x = x + self.pe[:, :x.size(1), :]
        return self.dropout(x)
