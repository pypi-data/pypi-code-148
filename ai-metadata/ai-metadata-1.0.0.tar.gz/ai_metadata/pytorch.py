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

import json
import numpy as np
import pandas as pd
from .base import MetadataModel, MiningFunction, ModelSerialization
from .utils import extract_major_minor_version, series_to_dataframe, normalize_shape, to_ndarray, shape_of


class PytorchModel(MetadataModel):
    """A wrapper of a Pytorch model
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
        import torch
        self.dtype = torch.Tensor(1).dtype

    @staticmethod
    def is_support(model) -> bool:
        try:
            from torch import nn
            return isinstance(model, nn.Module)
        except ImportError:
            return False

    def framework(self) -> str:
        return 'Pytorch'

    def framework_version(self) -> str:
        import torch
        return extract_major_minor_version(torch.__version__)

    def serialization(self) -> 'ModelSerialization':
        return ModelSerialization.PYTORCH

    def predict(self, data):
        prediction = self.predict_raw(data)
        shape = shape_of(prediction)
        if len(shape) > 1 and shape[1] > 1:
            prediction = np.argmax(prediction, axis=1)
        return prediction

    def predict_proba(self, data):
        if self.is_classification():
            return self.predict_raw(data)
        super().predict_proba(data)

    def predict_raw(self, data, **kwargs):
        import torch
        data = torch.from_numpy(to_ndarray(data)).type(self.dtype)
        return self.model(data).data.numpy()

    def inputs(self) -> dict:
        result = []

        columns = None
        shape = None
        sample = None
        if self.x_test is not None:
            x_test = series_to_dataframe(self.x_test)
            dtype = x_test.dtype
            shape = x_test.shape
            if isinstance(x_test, pd.DataFrame):
                row = x_test.iloc[0]
                columns = list(x_test.columns)
            else:
                row = x_test[0]
            sample = [row.tolist()]
        else:
            import torch
            dtype = torch.Tensor(1).numpy().dtype

        result.append({
            'name': None,
            'sample': sample,
            'type': dtype.name,
            'shape': normalize_shape(shape)
        })

        if columns is not None and result[-1]['sample'] is not None:
            result[-1]['columns'] = columns

        return result

    def targets(self) -> list:
        if self.y_test is None:
            return []

        result = []
        y_test = series_to_dataframe(self.y_test)
        if isinstance(y_test, pd.DataFrame):
            row = json.loads(y_test.iloc[0].to_json())
        else:
            row = y_test[0]

        result.append({
            'name': None,
            'sample': row.tolist(),
            'type': y_test.dtype.name,
            'shape': normalize_shape(y_test.shape)
        })

        return result

    def outputs(self) -> list:
        result = []

        if self.x_test is not None:
            shape = list(self.x_test.shape)
            if len(shape) > 0 and shape[0] > 1:
                shape[0] = 1

            import torch
            data = self.predict_raw(torch.randn(*shape))
            result.append(({
                'name': None,
                'type': data.dtype.name,
                'shape': normalize_shape(data.shape)
            }))
        return result

    def save_model(self, model_path) -> 'ModelSerialization':
        import torch
        torch.save(self.model.state_dict(), model_path)
        return self.serialization()

