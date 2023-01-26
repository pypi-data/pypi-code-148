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
import json
import os
from collections.abc import Mapping, Sequence, MutableSequence
from .base import MetadataModel, MiningFunction, ModelSerialization
from .utils import to_dataframe
from pypmml import Model, PmmlError


class PMMLModel(MetadataModel):
    """A wrapper of a PMML model
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
        self.pmml_model = Model.load(model)

    def __del__(self):
        if self.pmml_model:
            try:
                Model.close()
            except:
                pass

    @staticmethod
    def is_support(model) -> bool:
        try:
            Model.load(model)
            return True
        except PmmlError:
            Model.close()
            return False

    def model_type(self) -> str:
        return 'pmml'

    def framework(self) -> str:
        return 'PMML'

    def framework_version(self) -> str:
        return self.pmml_model.version

    def serialization(self) -> 'ModelSerialization':
        return ModelSerialization.PMML

    def function_name(self) -> 'MiningFunction':
        return self.pmml_model.functionName

    def runtime(self) -> str:
        return 'PyPMML'

    def algorithm(self) -> str:
        return self.pmml_model.modelElement

    def predict(self, data):
        prediction_name, prediction_index = self._get_prediction_col()

        prediction = self.predict_raw(data)
        if prediction_name is None:
            result = prediction
        elif isinstance(prediction, pd.DataFrame):
            result = prediction[prediction_name]
        elif isinstance(prediction, np.ndarray):
            result = prediction[:, prediction_index]
        elif isinstance(prediction, (dict, Mapping)):
            result = prediction[prediction_name]
        elif isinstance(prediction, list):
            if prediction:
                record = prediction[0]
                if isinstance(record, (list, Sequence, MutableSequence)):
                    result = [record[prediction_index] for record in prediction]
                else:
                    result = record[prediction_index]
            else:
                result = []
        return result

    def predict_proba(self, data):
        cols, indexes = self._get_probability_cols()
        if cols and indexes:
            prediction = self.predict_raw(data)

            if isinstance(prediction, pd.DataFrame):
                result = prediction[cols]
            elif isinstance(prediction, np.ndarray):
                result = prediction[:, indexes]
            elif isinstance(prediction, (dict, Mapping)):
                result = {x: prediction[x] for x in cols}
            elif isinstance(prediction, list):
                if prediction:
                    record = prediction[0]
                    if isinstance(record, (list, Sequence, MutableSequence)):
                        result = [[record[x] for x in indexes] for record in prediction]
                    else:
                        result = [prediction[x] for x in indexes]
                else:
                    result = []
            return result
        else:
            super().predict_proba(data)

    def predict_raw(self, data, **kwargs):
        return self.pmml_model.predict(data)

    def _get_prediction_col(self):
        output_fields = self.pmml_model.outputFields
        for index, item in enumerate(output_fields):
            if item.feature == 'predictedValue':
                return item.name, index
        return None, -1

    def _get_probability_cols(self):
        cols, indexes = [], []
        output_fields = self.pmml_model.outputFields
        for index, item in enumerate(output_fields):
            if item.feature == 'probability' and item.value is not None:
                cols.append(item.name)
                indexes.append(index)
        return cols, indexes

    def evaluate_metrics(self) -> dict:
        y_test = self.y_test
        x_test = self.x_test

        # Convert spark df to Pandas
        if self.data_test is not None:
            try:
                label_col = self.pmml_model.targetName
                if not label_col:
                    return {}

                pandas_data_test = self.data_test.toPandas()
                y_test = pandas_data_test[label_col]
                x_test = pandas_data_test
            except:
                return {}

        return self.evaluate_metrics_by_sklearn(x_test, y_test, self.function_name())

    def inputs(self) -> list:
        result = []

        row = None
        x_test = to_dataframe(self.x_test, self.data_test)
        if isinstance(x_test, pd.DataFrame):
            row = json.loads(x_test.iloc[0].to_json())
        elif isinstance(x_test, np.ndarray):
            row = x_test[0].tolist()
            if len(row) == len(self.pmml_model.inputFields):
                row = {field.name: value for field, value in zip(self.pmml_model.inputFields, row)}

        for x in self.pmml_model.inputFields:
            result.append(({
                'name': x.name,
                'sample': row.get(x.name) if row is not None else None,
                'type': x.dataType
            }))
        return result

    def targets(self) -> list:
        result = []

        row = None
        y_test = to_dataframe(self.y_test, self.data_test)
        if isinstance(y_test, pd.DataFrame):
            row = json.loads(y_test.iloc[0].to_json())

        for x in self.pmml_model.targetFields:
            result.append(({
                'name': x.name,
                'sample': row.get(x.name) if row is not None else None,
                'type': x.dataType
            }))
        return result

    def outputs(self) -> list:
        result = []
        for x in self.pmml_model.outputFields:
            result.append(({
                'name': x.name,
                'type': x.dataType
            }))
        return result

    def save_model(self, model_path) -> 'ModelSerialization':
        model = self.model
        if hasattr(self.model, 'read') and callable(self.model.read):
            model = self.model.read()
        if os.path.exists(self.model):
            with open(self.model, mode='rb') as f:
                model = f.read()
        mode = 'wb' if isinstance(model, (bytes, bytearray)) else 'w'
        with open(model_path, mode) as file:
            file.write(model)
        return self.serialization()

