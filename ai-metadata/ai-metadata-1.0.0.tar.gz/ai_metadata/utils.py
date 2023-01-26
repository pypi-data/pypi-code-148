#
# Copyright (c) 2023 AutoDeployAI
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import numpy as np
import pandas as pd


def shape_of(data) -> tuple:
    data = to_ndarray(data)
    if data is not None:
        return data.shape
    return ()


def to_ndarray(data) -> np.ndarray:
    if isinstance(data, np.ndarray) or data is None:
        return data
    elif isinstance(data, (pd.DataFrame, pd.Series)):
        return data.values
    else:
        return np.asarray(data)


def extract_major_minor_version(version: str) -> str:
    result = version
    elements = version.split('.')
    if len(elements) > 2:
        result = '{major}.{minor}'.format(major=elements[0], minor=elements[1])
    return result


def normalize_shape(shape) -> list:
    result = None
    if shape is not None and len(shape) > 1:
        result = []
        for idx, d in enumerate(shape):
            if idx == 0:
                result.append(None)
            else:
                result.append(d)
    return result


def series_to_dataframe(data):
    if isinstance(data, pd.Series):
        return pd.DataFrame(data)
    return data


def test_data_to_ndarray(x_y_test, data_test):
    data = to_dataframe(x_y_test, data_test)
    if isinstance(data, pd.DataFrame):
        return data.values
    return data


def to_dataframe(x_y_test, data_test):
    if x_y_test is None and data_test is not None:
        x_y_test = data_test.limit(1).toPandas()
    if isinstance(x_y_test, pd.Series):
        x_y_test = pd.DataFrame(x_y_test)
    return x_y_test


def is_compatible_shape(shape1, shape2):
    # could be tuple and list
    shape1 = list(shape1)
    shape2 = list(shape2)
    if len(shape1) > 1:
        shape1 = shape1[1:]
    if len(shape2) > 1:
        shape2 = shape2[1:]
    return elements_count(shape1) == elements_count(shape2)


def elements_count(shape):
    result = 1
    for n in shape:
        if isinstance(n, int):
            result *= n
    return result


def ndarray_or_dataframe(data):
    if data is not None:
        if isinstance(data, (np.ndarray, pd.DataFrame, pd.Series)):
            return data
        return np.asarray(data)
    return None


def convert_to_json_format(data: dict) -> dict:
    return {key: str(value) for key, value in data.items()}

