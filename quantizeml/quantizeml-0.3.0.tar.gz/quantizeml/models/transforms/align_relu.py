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
"""
Tools to align ReLU max_value to the maximum integer value the OutputQuantizer can use.
"""
from keras.layers import (ReLU, Conv2D, Conv2DTranspose, SeparableConv2D, DepthwiseConv2D, Dense,
                          Dropout, MaxPool2D, GlobalAvgPool2D)

from .. import deep_clone_model, get_layers_by_type, find_layer_config
from ...layers import PaddedConv2D, SeparableConv2DTranspose
from ...tensors import FixedPoint, floor_log2


def _get_surrounding_layer(layer, previous, supported_layers, skippable_layers):
    """ Finds the layer preceeding or following a target layer.

    Args:
        layer (keras.Layer): the layer of interest
        previous (bool): True to find the preceeding layer, False to find the layer that follows
        supported_layers (list): layer type that will support ReLU alignement
        skippable_layers (list): layer types that can be skipped

    Returns:
        keras.Layer: the layer preceeding or the layer following the layer of interest if valid,
        None otherwise
    """
    if previous:
        # Limit support to single inbound
        inbounds = layer.inbound_nodes
        if len(inbounds) != 1:
            return None
        surrounding_layer = inbounds[0].inbound_layers
    else:
        # Limit support to single outbound
        outbounds = layer.outbound_nodes
        if len(outbounds) != 1:
            return None
        surrounding_layer = outbounds[0].layer

    # If the layer is supported, it is a valid candidate
    if type(surrounding_layer) in supported_layers:
        return surrounding_layer
    # If the surrounding layer can be skipped, recursively call the function
    elif type(surrounding_layer) in skippable_layers:
        return _get_surrounding_layer(surrounding_layer, previous, supported_layers,
                                      skippable_layers)
    # If the surrounding layer is not supported, alignement cannot happen
    return None


def align_relu_max_value(model, q_config):
    """ Update the ReLU activations in the model so that their max values are closer to the maximum
    integer value the OutputQuantizer can use given in the quantization configuration.

    The ReLU max_value are replaced by the maximum value that the ReLU output quantizers can
    generate which is computed as:

    .. math::
        frac_bits = bitwidth - floor_log2(old_max_value)
        new_max_value = FixedPoint(FixedPoint.int_max(bitwidth), bitwidth , frac_bits)

    To compensate for that and preserve outputs:

        - the previous layer weights and bias are multiplied by new_max_value / old_max_value
        - the next layer weights are multiplied by old_max_value / new_max_value

    Args:
        model (keras.Model): the model to update
        q_config (dict): quantization configuration

    Returns:
        keras.Model: the model with ReLU activations updated.
    """
    # Define layers that will support weight rescaling induced by ReLU alignement
    supported_layers = (Conv2D, PaddedConv2D, Conv2DTranspose, SeparableConv2D, DepthwiseConv2D,
                        Dense, SeparableConv2DTranspose)

    # Define layers that can be skippped when looking for layers to compensate alignement
    skippable_layers = (Dropout, MaxPool2D, GlobalAvgPool2D)

    # Clone the model to apply modifications
    clone = deep_clone_model(model)

    # Get all ReLU layers present in the model and proceed to alignement
    relus = get_layers_by_type(clone, ReLU)
    for relu in relus:
        # Retrieve the surrounding layers: inbound and outbound layers must be compatible, meaning
        # they have weights where a rescaling will happen
        previous_layer = _get_surrounding_layer(relu, True, supported_layers, skippable_layers)
        next_layer = _get_surrounding_layer(relu, False, supported_layers, skippable_layers)
        if previous_layer is None or next_layer is None:
            continue

        # Get the ReLU quantization configuration
        relu_config = find_layer_config(relu.name, q_config)
        if (relu_config is None or relu_config.get('output_quantizer', None) is None or
                relu_config.get('output_quantizer').get('bitwidth', None) is None):
            continue

        # Compute the new max value that is closer to the maximum integer value the OutputQuantizer
        # can use
        old_max_value = relu.max_value
        bitwidth = relu_config['output_quantizer']['bitwidth']
        frac_bits = bitwidth - floor_log2(old_max_value)
        int_max = FixedPoint.int_max(bitwidth)
        new_max_value = FixedPoint(int_max, bitwidth, frac_bits).to_float().numpy()

        # Check that the values are different
        if new_max_value == old_max_value:
            continue

        # Set the max value in the layer
        relu.max_value = new_max_value

        # Compensate the max_value alignement by:
        #   - multiplying the previous layer weights and bias by new_max_value / old_max_value
        #   - multiplying the next layer weights by old_max_value / new_max_value
        indexes = [-1]
        if previous_layer.use_bias:
            indexes.append(-2)
        previous_weights = previous_layer.get_weights()
        for w in indexes:
            previous_weights[w] = previous_weights[w] * new_max_value / old_max_value
        previous_layer.set_weights(previous_weights)

        next_weights = next_layer.get_weights()
        next_weights[0] = next_weights[0] * old_max_value / new_max_value
        next_layer.set_weights(next_weights)

    return clone
