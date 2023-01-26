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

import pandas as pd
import numpy as np
from .base import MetadataModel, MiningFunction, ModelSerialization
from .utils import extract_major_minor_version, series_to_dataframe, is_compatible_shape, shape_of


class KerasModel(MetadataModel):
    """A wrapper of a Keras model
    """

    def __init__(self,
                 model,
                 mining_function: 'MiningFunction' = None,
                 x_test=None,
                 y_test=None,
                 data_test=None,
                 source_object=None,
                 **kwargs):
        super().__init__(model, mining_function, x_test, y_test, data_test, source_object, **kwargs)
        self.tf_keras = self._is_support_tf_keras(model)

    @staticmethod
    def is_support(model) -> bool:
        return KerasModel._is_support_keras(model) or \
               KerasModel._is_support_tf_keras(model)

    @staticmethod
    def _is_support_keras(model) -> bool:
        try:
            from keras.models import Model
            return isinstance(model, Model)
        except ImportError:
            return False

    @staticmethod
    def _is_support_tf_keras(model) -> bool:
        try:
            import tensorflow as tf
            return isinstance(model, tf.keras.Model)
        except ImportError:
            return False

    def framework(self) -> str:
        return 'Tensorflow' if self.tf_keras else 'Keras'

    def framework_version(self) -> str:
        if self.tf_keras:
            import tensorflow as tf
            return extract_major_minor_version(tf.keras.__version__)
        else:
            import keras
            return extract_major_minor_version(keras.__version__)

    def serialization(self) -> 'ModelSerialization':
        return ModelSerialization.HDF5

    def predict(self, data):
        prediction = self.predict_raw(data)

        shape = shape_of(prediction)
        if len(shape) > 1 and shape[1] > 1:
            prediction = np.argmax(prediction, axis=1)
        return prediction

    def predict_proba(self, data):
        if self.is_classification():
            return self.predict_raw(data)
        super().predict_proba()

    def inputs(self) -> list:
        result = []

        row = None
        columns = None
        if self.x_test is not None:
            x_test = series_to_dataframe(self.x_test)
            shape = x_test.shape
            if isinstance(x_test, pd.DataFrame):
                row = x_test.iloc[0]
                columns = list(x_test.columns)
            else:
                row = x_test[0]

        for idx, x in enumerate(self.model.inputs):
            name = x.name
            if hasattr(self.model, 'input_names'):
                name = self.model.input_names[idx]
            tensor_shape = self._normalize_tensor_shape(x.shape)
            result.append({
                'name': name,
                'sample': [row.tolist()] if row is not None and is_compatible_shape(tensor_shape, shape) else None,
                'type': np.dtype(x.dtype.as_numpy_dtype).name,
                'shape': tensor_shape
            })

            if columns is not None and result[-1]['sample'] is not None:
                result[-1]['columns'] = columns

        return result

    def outputs(self) -> list:
        result = []

        for idx, x in enumerate(self.model.outputs):
            name = x.name
            if hasattr(self.model, 'output_names'):
                name = self.model.output_names[idx]
            result.append(({
                'name': name,
                'type': np.dtype(x.dtype.as_numpy_dtype).name,
                'shape': self._normalize_tensor_shape(x.shape)
            }))
        return result

    def save_model(self, model_path) -> 'ModelSerialization':
        import tensorflow
        if tensorflow.__version__ >= '2':
            self.model.save(model_path, save_format='h5')
        else:
            self.model.save(model_path)
        return self.serialization()

    @staticmethod
    def _normalize_tensor_shape(tensor_shape):
        return [(d.value if hasattr(d, 'value') else d) for d in tensor_shape]

