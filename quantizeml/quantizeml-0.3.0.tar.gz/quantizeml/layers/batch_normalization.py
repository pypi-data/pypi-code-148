#!/usr/bin/env python
# ******************************************************************************
# Copyright 2023 Brainchip Holdings Ltd.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ******************************************************************************
import tensorflow as tf
import keras

from ..tensors import FixedPoint, QTensor, MAX_BUFFER_BITWIDTH
from .recorders import TensorRecorder
from .quantizers import (
    WeightQuantizer, AlignedWeightQuantizer, OutputQuantizer)

__all__ = ["QuantizedBatchNormalization"]


@tf.keras.utils.register_keras_serializable()
class QuantizedBatchNormalization(keras.layers.Layer):
    """Layer that normalizes its inputs, on the last axis.

    The normalization is applied like this:

    .. math::

        y = \\frac{(x - \\mu) \\cdot \\gamma}{\\sigma} + \\beta \\
            = \\frac{x \\cdot \\gamma}{\\sigma} - \\
              \\frac{\\mu\\cdot \\gamma}{\\gamma} + \\beta

    if we consider:

    .. math:: a = \\frac{\\gamma}{\\sigma}

    and

    .. math:: b = -\\frac{\\mu\\cdot \\gamma}{\\sigma} + \\beta


    The normalization can be re-written as:

    .. math:: y = a \\cdot x + b

    Note that this layer will hold variables with names gamma, beta,
    moving_mean (mu), and moving_variance (sigma), so they can be converted
    from a BatchNormalization layer. However, it's a and b that are going to
    be quantized.

    Args:
        axis (int, optional): The axis that was normalized on the
            BatchNormalization layer. The only supported value is the
            last dimension.
        epsilon (float, optional): Small value to avoid dividing by zero.
            Defaults to 1e-3.
        quant_config (dict, optional): the serialized quantization
            configuration. Defaults to empty configuration.
    """

    ignored_args = ["momentum",
                    "center",
                    "scale",
                    "beta_initializer",
                    "gamma_initializer",
                    "moving_mean_initializer",
                    "moving_variance_initializer",
                    "beta_regularizer",
                    "gamma_regularizer",
                    "beta_constraint",
                    "gamma_constraint",
                    "renorm",
                    "renorm_clipping",
                    "renorm_momentum",
                    "fused",
                    "trainable",
                    "virtual_batch_size",
                    "adjustment"
                    ]

    def __init__(self,
                 *args,
                 axis=-1,
                 epsilon=1e-3,
                 quant_config={},
                 **kwargs):
        super().__init__(*args, **kwargs)
        self.quant_config = quant_config
        out_quant_cfg = quant_config.get("output_quantizer", False)
        if out_quant_cfg:
            self.out_quantizer = OutputQuantizer(
                name="output_quantizer", **out_quant_cfg)
        else:
            self.out_quantizer = None
        self.a_quantizer = WeightQuantizer(
            name="a_quantizer", **quant_config["a_quantizer"])
        self.b_quantizer = AlignedWeightQuantizer(
            name="b_quantizer", **quant_config["b_quantizer"])
        self.buffer_bitwidth = self.quant_config.get(
            "buffer_bitwidth", MAX_BUFFER_BITWIDTH) - 1
        assert self.buffer_bitwidth > 0, \
            "The buffer_bitwidth must be a strictly positive integer."

        # Add objects that will store the shift values.
        self.input_shift = TensorRecorder(name="input_shift")

        # Define a small float number to avoid dividing by zero.
        self.epsilon = epsilon
        # Axis on which operation is applied
        self.axis = axis

    def build(self, input_shape):
        input_shape = tf.TensorShape(input_shape)
        rank = input_shape.rank

        if rank not in (3, 4):
            raise ValueError(
                "QuantizedBatchNormalization only supports 3D or 4D tensors. "
                f"Received tensor with shape: {tuple(input_shape)}.")

        # Normalize axis
        self.axis = keras.utils.tf_utils.validate_axis(self.axis, input_shape)
        # Check selected axis is valid
        if len(self.axis) != 1 and (self.axis[0] != rank - 1):
            raise ValueError("QuantizedBatchNormalization only supports axis "
                             "argument set to the last dimension.")

        # Shape for variables is always as if it was applied on the
        # last dimension.
        param_shape = input_shape[-1]

        # Add BN compatible weights
        # Gamma
        self.gamma = self.add_weight(
            name="gamma",
            shape=param_shape,
            dtype=tf.float32,
            initializer="ones",
            regularizer=None,
            constraint=None,
            trainable=True,
            experimental_autocast=False,
        )
        # Beta
        self.beta = self.add_weight(
            name="beta",
            shape=param_shape,
            dtype=tf.float32,
            initializer="zeros",
            regularizer=None,
            constraint=None,
            trainable=True,
            experimental_autocast=False,
        )
        # Mu = moving mean
        self.moving_mean = self.add_weight(
            name="moving_mean",
            shape=param_shape,
            dtype=tf.float32,
            initializer="zeros",
            regularizer=None,
            constraint=None,
            trainable=True,
            experimental_autocast=False,
        )
        # Sigma² = moving variance
        self.moving_variance = self.add_weight(
            name="moving_variance",
            shape=param_shape,
            dtype=tf.float32,
            initializer="ones",
            regularizer=None,
            constraint=None,
            trainable=True,
            experimental_autocast=False,
        )

    @property
    def sigma_rec(self):
        # Sigma reciprocal = 1 / sigma = 1 / sqrt(moving_variance + epsilon)
        sigma_rec = tf.math.rsqrt(self.moving_variance + self.epsilon)
        return sigma_rec

    @property
    def a(self):
        a_var = self.gamma * self.sigma_rec
        q_a = self.a_quantizer(a_var)
        return q_a

    def b(self, inputs):
        sigma_rec = self.sigma_rec
        b_var = -self.moving_mean * self.gamma * sigma_rec + self.beta
        q_b = self.b_quantizer(b_var, inputs)
        return q_b

    def call(self, inputs):
        # raise an error if the inputs are not QTensor
        if not isinstance(inputs, QTensor):
            raise TypeError(
                "QuantizedBatchNormalization only accepts QTensor inputs. " +
                f"Receives {type(inputs)} inputs.")

        # Calculation is equivalent to
        # y = (x - mu) * gamma / sigma + beta
        #   = x * gamma / sigma - mu * gamma / sigma + beta
        #
        # So if we consider
        # a = gamma / sigma
        # b = -mu * gamma / sigma + beta
        # Then the evaluation is just y = a * x + b.

        if isinstance(inputs, FixedPoint):
            # Expand the inputs to a higher bitwidth to avoid saturation and
            # align them
            inputs, shift = inputs.expand(self.buffer_bitwidth)
            self.input_shift(shift)
        else:
            # Just promote the QFloat inputs to avoid a saturation
            inputs = inputs.promote(self.buffer_bitwidth)

        # outputs = a * x
        outputs = tf.multiply(inputs, self.a)

        # quantize and retrieve b, aligned on the outputs to allow sum
        b = self.b(outputs)
        # y = outputs + b
        outputs = tf.add(outputs, b)

        if self.out_quantizer is not None:
            outputs = self.out_quantizer(outputs)
        return outputs

    def get_config(self):
        config = super().get_config()
        config.update({
            "quant_config": self.quant_config,
            "epsilon": self.epsilon,
            "axis": self.axis,
        })
        return config
