# Copyright 2019,2020,2021 Sony Corporation.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'rf_netAbs Add AvgPool CommonFunc ConcatV2 Conv2D Conv2DBackpropInput Greater Identity MatMul MaxPool Mean Mul Pad PadV2 Relu Reshape Rsqrt Select Slice Split SplitV SquaredDifference StopGradient Sub Transpose rf_net   :    rf_layers\n         rf_layers   :    rf_layers rf_layer_stmt\n                        |    rf_layer_stmt\n         rf_layer_stmt   :  rf_conv_2d\n                         |     rf_pool\n                         |     rf_conv_bn\n                         |     rf_p_relu\n                         |     rf_conv_transpose\n                         |     rf_bn\n                         |     rf_affine\n                         |     rf_binary_sigmoid\n                         |     CommonFunc\n                         |     Conv2D\n                         |     Split\n                         |     SplitV\n                         |     MaxPool\n                         |     AvgPool\n                         |     Add\n                         |     Pad\n                         |     Mul\n                         |     Identity\n                         |     Transpose\n                         |     Relu\n                         |     Abs\n                         |     Sub\n                         |     ConcatV2\n                         |     Slice\n                         |     Conv2DBackpropInput\n                         |     PadV2\n                         |     MatMul\n                         |     Reshape\n                         |     Greater\n                         |     Select\n                         |     Mean\n                         |     StopGradient\n                         |     SquaredDifference\n                         |     Rsqrt\n          rf_split_stmt     :    Split\n                             |    SplitV\n         rf_conv2d_loop_stmt     :   rf_conv2d_loop_stmt Conv2D\n                                    |   Conv2D\n         rf_conv_transpose  :    Transpose rf_split_stmt Conv2DBackpropInput Slice Identity Add Transpose\n                               |    Transpose rf_split_stmt Conv2DBackpropInput Slice Identity Transpose\n         rf_p_relu  :    Relu Abs Sub Mul Mul Add\n         rf_conv_bn  :    rf_conv_2d Mul Add\n         rf_conv_2d  :    Pad Transpose rf_split_stmt Conv2D Identity Add Transpose\n                        |   Pad Transpose rf_split_stmt Conv2D Identity Transpose\n                        |   Pad Transpose rf_split_stmt rf_conv2d_loop_stmt ConcatV2 Add Transpose\n                        |   Pad Transpose rf_split_stmt rf_conv2d_loop_stmt ConcatV2 Transpose\n         rf_pool_stmt     :    MaxPool\n                             |    AvgPool\n         rf_pool     :    Transpose rf_pool_stmt Transpose\n                        |    PadV2 Transpose rf_pool_stmt Transpose\n         rf_bn     :    Mul Add\n                      |    Mean StopGradient SquaredDifference Mean Add Rsqrt Mul Mul Mul Sub Add \n         rf_affine    :    Reshape Reshape MatMul Mul Add Reshape\n                         |    Reshape Reshape MatMul Mul Add Reshape Reshape Mul Add\n         rf_binary_sigmoid     :    Greater Select\n        '

_lr_action_items = {'CommonFunc': ([0, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 41, 51, 53, 55, 65, 75, 77, 79, 81, 82, 84, 85, 86, 91, 94, ], [12, 12, -3, -4, -5, -6, -7, -8, -9, -10, -11, -12, -13, -14, -15, -16, -17, -18, -19, -20, -21, -22, -23, -24, -25, -26, -27, -28, -29, -30, -31, -32, -33, -34, -35, -36, -37, -2, -54, -58, -45, -52, -53, -47, -49, -43, -44, -56, -46, -48, -42, -57, -55, ]), 'Conv2D': ([0, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 41, 46, 47, 51, 53, 54, 55, 61, 62, 65, 70, 75, 77, 79, 81, 82, 84, 85, 86, 91, 94, ], [13, 13, -3, -4, -5, -6, -7, -8, -9, -10, -11, -12, -13, -14, -15, -16, -17, -18, -19, -20, -21, -22, -23, -24, -25, -26, -27, -28, -29, -30, -31, -32, -33, -34, -35, -36, -37, -2, -54, -38, -39, -58, -45, 61, -52, -41, 70, -53, -40, -47, -49, -43, -44, -56, -46, -48, -42, -57, -55, ]), 'Split': ([0, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 40, 41, 51, 53, 55, 65, 75, 77, 79, 81, 82, 84, 85, 86, 91, 94, ], [14, 14, -3, -4, -5, -6, -7, -8, -9, -10, -11, -12, -13, -14, -15, -16, -17, -18, -19, -20, -21, 46, -23, -24, -25, -26, -27, -28, -29, -30, -31, -32, -33, -34, -35, -36, -37, -2, 46, -54, -58, -45, -52, -53, -47, -49, -43, -44, -56, -46, -48, -42, -57, -55, ]), 'SplitV': ([0, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 40, 41, 51, 53, 55, 65, 75, 77, 79, 81, 82, 84, 85, 86, 91, 94, ], [15, 15, -3, -4, -5, -6, -7, -8, -9, -10, -11, -12, -13, -14, -15, -16, -17, -18, -19, -20, -21, 47, -23, -24, -25, -26, -27, -28, -29, -30, -31, -32, -33, -34, -35, -36, -37, -2, 47, -54, -58, -45, -52, -53, -47, -49, -43, -44, -56, -46, -48, -42, -57, -55, ]), 'MaxPool': ([0, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 41, 49, 51, 53, 55, 65, 75, 77, 79, 81, 82, 84, 85, 86, 91, 94, ], [16, 16, -3, -4, -5, -6, -7, -8, -9, -10, -11, -12, -13, -14, -15, -16, -17, -18, -19, -20, -21, 44, -23, -24, -25, -26, -27, -28, -29, -30, -31, -32, -33, -34, -35, -36, -37, -2, -54, 44, -58, -45, -52, -53, -47, -49, -43, -44, -56, -46, -48, -42, -57, -55, ]), 'AvgPool': ([0, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 41, 49, 51, 53, 55, 65, 75, 77, 79, 81, 82, 84, 85, 86, 91, 94, ], [17, 17, -3, -4, -5, -6, -7, -8, -9, -10, -11, -12, -13, -14, -15, -16, -17, -18, -19, -20, -21, 45, -23, -24, -25, -26, -27, -28, -29, -30, -31, -32, -33, -34, -35, -36, -37, -2, -54, 45, -58, -45, -52, -53, -47, -49, -43, -44, -56, -46, -48, -42, -57, -55, ]), 'Add': ([0, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 41, 51, 53, 55, 65, 66, 67, 68, 69, 71, 72, 75, 77, 79, 81, 82, 84, 85, 86, 89, 91, 93, 94, ], [18, 18, -3, -4, -5, -6, -7, -8, -9, -10, -11, -12, -13, -14, -15, -16, -17, -18, -19, 41, -21, -22, -23, -24, -25, -26, -27, -28, -29, -30, -31, -32, -33, -34, -35, -36, -37, -2, 53, -54, -58, -45, -52, -53, 73, 74, 76, 78, 80, 81, -47, -49, -43, -44, -56, -46, -48, -42, 91, -57, 94, -55, ]), 'Pad': ([0, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 41, 51, 53, 55, 65, 75, 77, 79, 81, 82, 84, 85, 86, 91, 94, ], [19, 19, -3, -4, -5, -6, -7, -8, -9, -10, -11, -12, -13, -14, -15, -16, -17, -18, -19, -20, -21, -22, -23, -24, -25, -26, -27, -28, -29, -30, -31, -32, -33, -34, -35, -36, -37, -2, -54, -58, -45, -52, -53, -47, -49, -43, -44, -56, -46, -48, -42, -57, -55, ]), 'Mul': ([0, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 41, 51, 53, 55, 57, 59, 64, 65, 75, 77, 79, 81, 82, 83, 84, 85, 86, 87, 88, 90, 91, 94, ], [20, 20, -3, 39, -5, -6, -7, -8, -9, -10, -11, -12, -13, -14, -15, -16, -17, -18, -19, -20, -21, -22, -23, -24, -25, -26, -27, -28, -29, -30, -31, -32, -33, -34, -35, -36, -37, -2, -54, -58, -45, -52, 64, 66, 72, -53, -47, -49, -43, -44, -56, 88, -46, -48, -42, 89, 90, 92, -57, -55, ]), 'Identity': ([0, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 41, 51, 53, 55, 61, 63, 65, 75, 77, 79, 81, 82, 84, 85, 86, 91, 94, ], [21, 21, -3, -4, -5, -6, -7, -8, -9, -10, -11, -12, -13, -14, -15, -16, -17, -18, -19, -20, -21, -22, -23, -24, -25, -26, -27, -28, -29, -30, -31, -32, -33, -34, -35, -36, -37, -2, -54, -58, -45, -52, 68, 71, -53, -47, -49, -43, -44, -56, -46, -48, -42, -57, -55, ]), 'Transpose': ([0, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 41, 42, 44, 45, 51, 53, 55, 58, 65, 68, 69, 71, 75, 76, 77, 78, 79, 80, 81, 82, 84, 85, 86, 91, 94, ], [22, 22, -3, -4, -5, -6, -7, -8, -9, -10, -11, -12, -13, -14, -15, -16, -17, -18, 40, -20, -21, -22, -23, -24, -25, -26, -27, -28, 49, -30, -31, -32, -33, -34, -35, -36, -37, -2, -54, 55, -50, -51, -58, -45, -52, 65, -53, 75, 77, 79, -47, 84, -49, 85, -43, 86, -44, -56, -46, -48, -42, -57, -55, ]), 'Relu': ([0, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 41, 51, 53, 55, 65, 75, 77, 79, 81, 82, 84, 85, 86, 91, 94, ], [23, 23, -3, -4, -5, -6, -7, -8, -9, -10, -11, -12, -13, -14, -15, -16, -17, -18, -19, -20, -21, -22, -23, -24, -25, -26, -27, -28, -29, -30, -31, -32, -33, -34, -35, -36, -37, -2, -54, -58, -45, -52, -53, -47, -49, -43, -44, -56, -46, -48, -42, -57, -55, ]), 'Abs': ([0, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 41, 51, 53, 55, 65, 75, 77, 79, 81, 82, 84, 85, 86, 91, 94, ], [24, 24, -3, -4, -5, -6, -7, -8, -9, -10, -11, -12, -13, -14, -15, -16, -17, -18, -19, -20, -21, -22, 48, -24, -25, -26, -27, -28, -29, -30, -31, -32, -33, -34, -35, -36, -37, -2, -54, -58, -45, -52, -53, -47, -49, -43, -44, -56, -46, -48, -42, -57, -55, ]), 'Sub': ([0, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37,
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             38, 41, 48, 51, 53, 55, 65, 75, 77, 79, 81, 82, 84, 85, 86, 91, 92, 94, ], [25, 25, -3, -4, -5, -6, -7, -8, -9, -10, -11, -12, -13, -14, -15, -16, -17, -18, -19, -20, -21, -22, -23, -24, -25, -26, -27, -28, -29, -30, -31, -32, -33, -34, -35, -36, -37, -2, -54, 57, -58, -45, -52, -53, -47, -49, -43, -44, -56, -46, -48, -42, -57, 93, -55, ]), 'ConcatV2': ([0, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 41, 51, 53, 55, 61, 62, 65, 70, 75, 77, 79, 81, 82, 84, 85, 86, 91, 94, ], [26, 26, -3, -4, -5, -6, -7, -8, -9, -10, -11, -12, -13, -14, -15, -16, -17, -18, -19, -20, -21, -22, -23, -24, -25, -26, -27, -28, -29, -30, -31, -32, -33, -34, -35, -36, -37, -2, -54, -58, -45, -52, -41, 69, -53, -40, -47, -49, -43, -44, -56, -46, -48, -42, -57, -55, ]), 'Slice': ([0, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 41, 51, 53, 55, 56, 65, 75, 77, 79, 81, 82, 84, 85, 86, 91, 94, ], [27, 27, -3, -4, -5, -6, -7, -8, -9, -10, -11, -12, -13, -14, -15, -16, -17, -18, -19, -20, -21, -22, -23, -24, -25, -26, -27, -28, -29, -30, -31, -32, -33, -34, -35, -36, -37, -2, -54, -58, -45, -52, 63, -53, -47, -49, -43, -44, -56, -46, -48, -42, -57, -55, ]), 'Conv2DBackpropInput': ([0, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 41, 43, 46, 47, 51, 53, 55, 65, 75, 77, 79, 81, 82, 84, 85, 86, 91, 94, ], [28, 28, -3, -4, -5, -6, -7, -8, -9, -10, -11, -12, -13, -14, -15, -16, -17, -18, -19, -20, -21, -22, -23, -24, -25, -26, -27, -28, -29, -30, -31, -32, -33, -34, -35, -36, -37, -2, -54, 56, -38, -39, -58, -45, -52, -53, -47, -49, -43, -44, -56, -46, -48, -42, -57, -55, ]), 'PadV2': ([0, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 41, 51, 53, 55, 65, 75, 77, 79, 81, 82, 84, 85, 86, 91, 94, ], [29, 29, -3, -4, -5, -6, -7, -8, -9, -10, -11, -12, -13, -14, -15, -16, -17, -18, -19, -20, -21, -22, -23, -24, -25, -26, -27, -28, -29, -30, -31, -32, -33, -34, -35, -36, -37, -2, -54, -58, -45, -52, -53, -47, -49, -43, -44, -56, -46, -48, -42, -57, -55, ]), 'MatMul': ([0, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 41, 50, 51, 53, 55, 65, 75, 77, 79, 81, 82, 84, 85, 86, 91, 94, ], [30, 30, -3, -4, -5, -6, -7, -8, -9, -10, -11, -12, -13, -14, -15, -16, -17, -18, -19, -20, -21, -22, -23, -24, -25, -26, -27, -28, -29, -30, -31, -32, -33, -34, -35, -36, -37, -2, -54, 59, -58, -45, -52, -53, -47, -49, -43, -44, -56, -46, -48, -42, -57, -55, ]), 'Reshape': ([0, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 41, 51, 53, 55, 65, 73, 75, 77, 79, 81, 82, 84, 85, 86, 91, 94, ], [31, 31, -3, -4, -5, -6, -7, -8, -9, -10, -11, -12, -13, -14, -15, -16, -17, -18, -19, -20, -21, -22, -23, -24, -25, -26, -27, -28, -29, -30, 50, -32, -33, -34, -35, -36, -37, -2, -54, -58, -45, -52, -53, 82, -47, -49, -43, -44, 87, -46, -48, -42, -57, -55, ]), 'Greater': ([0, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 41, 51, 53, 55, 65, 75, 77, 79, 81, 82, 84, 85, 86, 91, 94, ], [32, 32, -3, -4, -5, -6, -7, -8, -9, -10, -11, -12, -13, -14, -15, -16, -17, -18, -19, -20, -21, -22, -23, -24, -25, -26, -27, -28, -29, -30, -31, -32, -33, -34, -35, -36, -37, -2, -54, -58, -45, -52, -53, -47, -49, -43, -44, -56, -46, -48, -42, -57, -55, ]), 'Select': ([0, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 41, 51, 53, 55, 65, 75, 77, 79, 81, 82, 84, 85, 86, 91, 94, ], [33, 33, -3, -4, -5, -6, -7, -8, -9, -10, -11, -12, -13, -14, -15, -16, -17, -18, -19, -20, -21, -22, -23, -24, -25, -26, -27, -28, -29, -30, -31, 51, -33, -34, -35, -36, -37, -2, -54, -58, -45, -52, -53, -47, -49, -43, -44, -56, -46, -48, -42, -57, -55, ]), 'Mean': ([0, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 41, 51, 53, 55, 60, 65, 75, 77, 79, 81, 82, 84, 85, 86, 91, 94, ], [34, 34, -3, -4, -5, -6, -7, -8, -9, -10, -11, -12, -13, -14, -15, -16, -17, -18, -19, -20, -21, -22, -23, -24, -25, -26, -27, -28, -29, -30, -31, -32, -33, -34, -35, -36, -37, -2, -54, -58, -45, -52, 67, -53, -47, -49, -43, -44, -56, -46, -48, -42, -57, -55, ]), 'StopGradient': ([0, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 41, 51, 53, 55, 65, 75, 77, 79, 81, 82, 84, 85, 86, 91, 94, ], [35, 35, -3, -4, -5, -6, -7, -8, -9, -10, -11, -12, -13, -14, -15, -16, -17, -18, -19, -20, -21, -22, -23, -24, -25, -26, -27, -28, -29, -30, -31, -32, -33, 52, -35, -36, -37, -2, -54, -58, -45, -52, -53, -47, -49, -43, -44, -56, -46, -48, -42, -57, -55, ]), 'SquaredDifference': ([0, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 41, 51, 52, 53, 55, 65, 75, 77, 79, 81, 82, 84, 85, 86, 91, 94, ], [36, 36, -3, -4, -5, -6, -7, -8, -9, -10, -11, -12, -13, -14, -15, -16, -17, -18, -19, -20, -21, -22, -23, -24, -25, -26, -27, -28, -29, -30, -31, -32, -33, -34, -35, -36, -37, -2, -54, -58, 60, -45, -52, -53, -47, -49, -43, -44, -56, -46, -48, -42, -57, -55, ]), 'Rsqrt': ([0, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 41, 51, 53, 55, 65, 74, 75, 77, 79, 81, 82, 84, 85, 86, 91, 94, ], [37, 37, -3, -4, -5, -6, -7, -8, -9, -10, -11, -12, -13, -14, -15, -16, -17, -18, -19, -20, -21, -22, -23, -24, -25, -26, -27, -28, -29, -30, -31, -32, -33, -34, -35, -36, -37, -2, -54, -58, -45, -52, -53, 83, -47, -49, -43, -44, -56, -46, -48, -42, -57, -55, ]), '$end': ([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 41, 51, 53, 55, 65, 75, 77, 79, 81, 82, 84, 85, 86, 91, 94, ], [0, -1, -3, -4, -5, -6, -7, -8, -9, -10, -11, -12, -13, -14, -15, -16, -17, -18, -19, -20, -21, -22, -23, -24, -25, -26, -27, -28, -29, -30, -31, -32, -33, -34, -35, -36, -37, -2, -54, -58, -45, -52, -53, -47, -49, -43, -44, -56, -46, -48, -42, -57, -55, ]), }

_lr_action = {}
for _k, _v in _lr_action_items.items():
    for _x, _y in zip(_v[0], _v[1]):
        if not _x in _lr_action:
            _lr_action[_x] = {}
        _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'rf_net': ([0, ], [1, ]), 'rf_layers': ([0, ], [2, ]), 'rf_layer_stmt': ([0, 2, ], [3, 38, ]), 'rf_conv_2d': ([0, 2, ], [4, 4, ]), 'rf_pool': ([0, 2, ], [5, 5, ]), 'rf_conv_bn': ([0, 2, ], [6, 6, ]), 'rf_p_relu': ([0, 2, ], [7, 7, ]), 'rf_conv_transpose': (
    [0, 2, ], [8, 8, ]), 'rf_bn': ([0, 2, ], [9, 9, ]), 'rf_affine': ([0, 2, ], [10, 10, ]), 'rf_binary_sigmoid': ([0, 2, ], [11, 11, ]), 'rf_pool_stmt': ([22, 49, ], [42, 58, ]), 'rf_split_stmt': ([22, 40, ], [43, 54, ]), 'rf_conv2d_loop_stmt': ([54, ], [62, ]), }

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
    for _x, _y in zip(_v[0], _v[1]):
        if not _x in _lr_goto:
            _lr_goto[_x] = {}
        _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> rf_net", "S'", 1, None, None, None),
  ('rf_net -> rf_layers', 'rf_net', 1, 'p_rf_net', 'refine_parser.py', 23),
  ('rf_layers -> rf_layers rf_layer_stmt', 'rf_layers',
   2, 'p_rf_layers', 'refine_parser.py', 28),
  ('rf_layers -> rf_layer_stmt', 'rf_layers',
   1, 'p_rf_layers', 'refine_parser.py', 29),
  ('rf_layer_stmt -> rf_conv_2d', 'rf_layer_stmt',
   1, 'p_rf_layer_stmt', 'refine_parser.py', 38),
  ('rf_layer_stmt -> rf_pool', 'rf_layer_stmt',
   1, 'p_rf_layer_stmt', 'refine_parser.py', 39),
  ('rf_layer_stmt -> rf_conv_bn', 'rf_layer_stmt',
   1, 'p_rf_layer_stmt', 'refine_parser.py', 40),
  ('rf_layer_stmt -> rf_p_relu', 'rf_layer_stmt',
   1, 'p_rf_layer_stmt', 'refine_parser.py', 41),
  ('rf_layer_stmt -> rf_conv_transpose', 'rf_layer_stmt',
   1, 'p_rf_layer_stmt', 'refine_parser.py', 42),
  ('rf_layer_stmt -> rf_bn', 'rf_layer_stmt', 1,
   'p_rf_layer_stmt', 'refine_parser.py', 43),
  ('rf_layer_stmt -> rf_affine', 'rf_layer_stmt',
   1, 'p_rf_layer_stmt', 'refine_parser.py', 44),
  ('rf_layer_stmt -> rf_binary_sigmoid', 'rf_layer_stmt',
   1, 'p_rf_layer_stmt', 'refine_parser.py', 45),
  ('rf_layer_stmt -> CommonFunc', 'rf_layer_stmt',
   1, 'p_rf_layer_stmt', 'refine_parser.py', 46),
  ('rf_layer_stmt -> Conv2D', 'rf_layer_stmt',
   1, 'p_rf_layer_stmt', 'refine_parser.py', 47),
  ('rf_layer_stmt -> Split', 'rf_layer_stmt', 1,
   'p_rf_layer_stmt', 'refine_parser.py', 48),
  ('rf_layer_stmt -> SplitV', 'rf_layer_stmt',
   1, 'p_rf_layer_stmt', 'refine_parser.py', 49),
  ('rf_layer_stmt -> MaxPool', 'rf_layer_stmt',
   1, 'p_rf_layer_stmt', 'refine_parser.py', 50),
  ('rf_layer_stmt -> AvgPool', 'rf_layer_stmt',
   1, 'p_rf_layer_stmt', 'refine_parser.py', 51),
  ('rf_layer_stmt -> Add', 'rf_layer_stmt', 1,
   'p_rf_layer_stmt', 'refine_parser.py', 52),
  ('rf_layer_stmt -> Pad', 'rf_layer_stmt', 1,
   'p_rf_layer_stmt', 'refine_parser.py', 53),
  ('rf_layer_stmt -> Mul', 'rf_layer_stmt', 1,
   'p_rf_layer_stmt', 'refine_parser.py', 54),
  ('rf_layer_stmt -> Identity', 'rf_layer_stmt',
   1, 'p_rf_layer_stmt', 'refine_parser.py', 55),
  ('rf_layer_stmt -> Transpose', 'rf_layer_stmt',
   1, 'p_rf_layer_stmt', 'refine_parser.py', 56),
  ('rf_layer_stmt -> Relu', 'rf_layer_stmt', 1,
   'p_rf_layer_stmt', 'refine_parser.py', 57),
  ('rf_layer_stmt -> Abs', 'rf_layer_stmt', 1,
   'p_rf_layer_stmt', 'refine_parser.py', 58),
  ('rf_layer_stmt -> Sub', 'rf_layer_stmt', 1,
   'p_rf_layer_stmt', 'refine_parser.py', 59),
  ('rf_layer_stmt -> ConcatV2', 'rf_layer_stmt',
   1, 'p_rf_layer_stmt', 'refine_parser.py', 60),
  ('rf_layer_stmt -> Slice', 'rf_layer_stmt', 1,
   'p_rf_layer_stmt', 'refine_parser.py', 61),
  ('rf_layer_stmt -> Conv2DBackpropInput', 'rf_layer_stmt',
   1, 'p_rf_layer_stmt', 'refine_parser.py', 62),
  ('rf_layer_stmt -> PadV2', 'rf_layer_stmt', 1,
   'p_rf_layer_stmt', 'refine_parser.py', 63),
  ('rf_layer_stmt -> MatMul', 'rf_layer_stmt',
   1, 'p_rf_layer_stmt', 'refine_parser.py', 64),
  ('rf_layer_stmt -> Reshape', 'rf_layer_stmt',
   1, 'p_rf_layer_stmt', 'refine_parser.py', 65),
  ('rf_layer_stmt -> Greater', 'rf_layer_stmt',
   1, 'p_rf_layer_stmt', 'refine_parser.py', 66),
  ('rf_layer_stmt -> Select', 'rf_layer_stmt',
   1, 'p_rf_layer_stmt', 'refine_parser.py', 67),
  ('rf_layer_stmt -> Mean', 'rf_layer_stmt', 1,
   'p_rf_layer_stmt', 'refine_parser.py', 68),
  ('rf_layer_stmt -> StopGradient', 'rf_layer_stmt',
   1, 'p_rf_layer_stmt', 'refine_parser.py', 69),
  ('rf_layer_stmt -> SquaredDifference', 'rf_layer_stmt',
   1, 'p_rf_layer_stmt', 'refine_parser.py', 70),
  ('rf_layer_stmt -> Rsqrt', 'rf_layer_stmt', 1,
   'p_rf_layer_stmt', 'refine_parser.py', 71),
  ('rf_split_stmt -> Split', 'rf_split_stmt', 1,
   'p_rf_split_stmt', 'refine_parser.py', 76),
  ('rf_split_stmt -> SplitV', 'rf_split_stmt',
   1, 'p_rf_split_stmt', 'refine_parser.py', 77),
  ('rf_conv2d_loop_stmt -> rf_conv2d_loop_stmt Conv2D',
   'rf_conv2d_loop_stmt', 2, 'p_rf_conv2d_loop_stmt', 'refine_parser.py', 82),
  ('rf_conv2d_loop_stmt -> Conv2D', 'rf_conv2d_loop_stmt',
   1, 'p_rf_conv2d_loop_stmt', 'refine_parser.py', 83),
  ('rf_conv_transpose -> Transpose rf_split_stmt Conv2DBackpropInput Slice Identity Add Transpose',
   'rf_conv_transpose', 7, 'p_rf_conv_transpose', 'refine_parser.py', 88),
  ('rf_conv_transpose -> Transpose rf_split_stmt Conv2DBackpropInput Slice Identity Transpose',
   'rf_conv_transpose', 6, 'p_rf_conv_transpose', 'refine_parser.py', 89),
  ('rf_p_relu -> Relu Abs Sub Mul Mul Add', 'rf_p_relu',
   6, 'p_rf_p_relu', 'refine_parser.py', 94),
  ('rf_conv_bn -> rf_conv_2d Mul Add', 'rf_conv_bn',
   3, 'p_rf_conv_bn', 'refine_parser.py', 99),
  ('rf_conv_2d -> Pad Transpose rf_split_stmt Conv2D Identity Add Transpose',
   'rf_conv_2d', 7, 'p_rf_conv_2d', 'refine_parser.py', 104),
  ('rf_conv_2d -> Pad Transpose rf_split_stmt Conv2D Identity Transpose',
   'rf_conv_2d', 6, 'p_rf_conv_2d', 'refine_parser.py', 105),
  ('rf_conv_2d -> Pad Transpose rf_split_stmt rf_conv2d_loop_stmt ConcatV2 Add Transpose',
   'rf_conv_2d', 7, 'p_rf_conv_2d', 'refine_parser.py', 106),
  ('rf_conv_2d -> Pad Transpose rf_split_stmt rf_conv2d_loop_stmt ConcatV2 Transpose',
   'rf_conv_2d', 6, 'p_rf_conv_2d', 'refine_parser.py', 107),
  ('rf_pool_stmt -> MaxPool', 'rf_pool_stmt', 1,
   'p_rf_pool_stmt', 'refine_parser.py', 112),
  ('rf_pool_stmt -> AvgPool', 'rf_pool_stmt', 1,
   'p_rf_pool_stmt', 'refine_parser.py', 113),
  ('rf_pool -> Transpose rf_pool_stmt Transpose',
   'rf_pool', 3, 'p_rf_pool', 'refine_parser.py', 118),
  ('rf_pool -> PadV2 Transpose rf_pool_stmt Transpose',
   'rf_pool', 4, 'p_rf_pool', 'refine_parser.py', 119),
  ('rf_bn -> Mul Add', 'rf_bn', 2, 'p_rf_bn', 'refine_parser.py', 124),
  ('rf_bn -> Mean StopGradient SquaredDifference Mean Add Rsqrt Mul Mul Mul Sub Add',
   'rf_bn', 11, 'p_rf_bn', 'refine_parser.py', 125),
  ('rf_affine -> Reshape Reshape MatMul Mul Add Reshape',
   'rf_affine', 6, 'p_rf_affine', 'refine_parser.py', 130),
  ('rf_affine -> Reshape Reshape MatMul Mul Add Reshape Reshape Mul Add',
   'rf_affine', 9, 'p_rf_affine', 'refine_parser.py', 131),
  ('rf_binary_sigmoid -> Greater Select', 'rf_binary_sigmoid',
   2, 'p_rf_binary_sigmoid', 'refine_parser.py', 136),
]
