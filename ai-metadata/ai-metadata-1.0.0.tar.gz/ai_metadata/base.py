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

from abc import ABC, abstractmethod
import sys
import json
import pandas as pd
import numpy as np
from enum import Enum
import logging
import traceback

from .utils import ndarray_or_dataframe, series_to_dataframe, normalize_shape, convert_to_json_format, to_ndarray


class MiningFunction(str, Enum):
    """Mining function types."""
    UNKNOWN = 'unknown'
    CLASSIFICATION = 'classification'
    REGRESSION = 'regression'
    CLUSTERING = 'clustering'
    TIMESERIES = 'timeSeries'

    @staticmethod
    def infer_mining_function(y) -> 'MiningFunction':
        if y is None:
            return MiningFunction.UNKNOWN

        y = to_ndarray(y)
        if y.ndim >= 2:
            return MiningFunction.CLASSIFICATION if y.shape[y.ndim - 1] > 1 else MiningFunction.REGRESSION

        # float numbers are treated as a regression problem
        return MiningFunction.REGRESSION if y.dtype.kind in 'fc' else MiningFunction.CLASSIFICATION


class ModelSerialization(str, Enum):
    """Supported types of model serialization"""
    PICKLE = 'pickle'
    JOBLIB = 'joblib'
    SPARK = 'spark'
    HDF5 = 'hdf5'
    XGBOOST = 'xgboost'
    LIGHTGBM = 'lightgbm'
    PMML = 'pmml'
    ONNX = 'onnx'
    PYTORCH = 'pytorch'


class MetadataModel(ABC):
    """Base class for wrapping the internal model object from various frameworks"""
    def __init__(self,
                 model,
                 mining_function: 'MiningFunction' = None,
                 x_test=None,
                 y_test=None,
                 data_test=None,
                 source_object=None,
                 **kwargs):
        if not self.is_support(model):
            raise ValueError(f'The model "{model.__class__.__name__}" is not a valid model of {self.framework()}.')

        if mining_function is not None:
            if mining_function not in MiningFunction:
                raise ValueError(f'mining_function should be one of {MiningFunction}, {mining_function} was given')
        else:
            mining_function = MiningFunction.infer_mining_function(y_test)

        if x_test is None and 'X_test' in kwargs:
            x_test = kwargs['X_test']

        self.model = model
        self.mining_function = mining_function
        self.x_test = ndarray_or_dataframe(x_test)
        self.y_test = ndarray_or_dataframe(y_test)
        self.data_test = data_test
        self.source_object = source_object

    @staticmethod
    def wrap(model,
             mining_function: 'MiningFunction' = None,
             x_test=None,
             y_test=None,
             data_test=None,
             source_object=None,
             **kwargs) -> 'MetadataModel':
        """
        Wrap the internal model object from various frameworks
        :param model: The model object
        :param mining_function: 'classification', 'regression', 'clustering'.
                Set the mining function of the model, could be inferred when not specified
        :param x_test: {array-like, sparse matrix}, shape (n_samples, n_features)
            Perform prediction on samples in X_test, predicted labels or estimated target values returned by the model
        :param y_test: 1d array-like, or label indicator array / sparse matrix.
            Ground truth (correct) target values.
        :param data_test: Test dataset, which is an instance of :py:class:`pyspark.sql.DataFrame`
            Used by models of PySpark
        :param source_object: An optional object's source code to save (class or function). Note: Class is not supported
            in the Jupyter notebook, while you can use a function that returns an instance of your model class
        :param kwargs: Extra named parameters, for example "X_test" is identical to "x_test"
        :return: An instance of wrapped metadata model that provides methods to retrieve metadata of the internal model.
        """
        from .lightgbm import LightGBMModel
        from .xgboost import XGBoostModel
        from .sklearn import SKLearnModel
        from .spark import SparkModel
        from .keras import KerasModel
        from .pytorch import PytorchModel
        from .pmml import PMMLModel
        from .onnx import ONNXModel
        from .custom import CustomModel

        # The order of such list is significant, do not change it!!!
        candidates = (XGBoostModel, LightGBMModel, SKLearnModel, SparkModel, KerasModel, PytorchModel,
                      PMMLModel, ONNXModel, CustomModel)

        for cls in candidates:
            if cls.is_support(model):
                return cls(model=model,
                           mining_function=mining_function,
                           x_test=x_test,
                           y_test=y_test,
                           data_test=data_test,
                           source_object=source_object,
                           **kwargs)
        return None

    @staticmethod
    def is_support(model) -> bool:
        return False

    def is_sklearn_format(self) -> bool:
        return False

    def is_pipeline_model(self) -> bool:
        return False

    def model_type(self) -> str:
        return f'{self.framework().lower()}'

    @abstractmethod
    def framework(self) -> str:
        raise NotImplementedError()

    @abstractmethod
    def framework_version(self) -> str:
        raise NotImplementedError()

    @abstractmethod
    def serialization(self) -> 'ModelSerialization':
        raise NotImplementedError()

    def function_name(self) -> 'MiningFunction':
        return self.mining_function

    def is_classification(self) -> bool:
        return self.function_name() == MiningFunction.CLASSIFICATION

    def runtime(self) -> str:
        return 'Python{major}.{minor}'.format(major=sys.version_info[0], minor=sys.version_info[1])

    def algorithm(self) -> str:
        return self.model.__class__.__name__

    def predict(self, data):
        return self.predict_raw(data)

    def predict_proba(self, data):
        raise AttributeError(f'The predict_proba not supported by the internal model "{self.algorithm()}"')

    def predict_raw(self, data, **kwargs):
        return self.model.predict(data)

    def evaluate_metrics(self) -> dict:
        return self.evaluate_metrics_by_sklearn(self.x_test, self.y_test, self.function_name())

    def inputs(self) -> list:
        if self.x_test is None:
            return []

        result = []
        x_test = series_to_dataframe(self.x_test)
        if isinstance(x_test, pd.DataFrame):
            row = json.loads(x_test.iloc[0].to_json())
            cols = x_test.columns
            for x in cols:
                result.append({
                    'name': x,
                    'sample': row[x],
                    'type': x_test[x].dtype.name
                })
        else:  # numpy array with multiple dimensions
            row = x_test[0].tolist()
            result.append({
                'name': None,
                'sample': [row],
                'type': x_test.dtype.name,
                'shape': normalize_shape(x_test.shape)
            })

        return result

    def targets(self) -> list:
        if self.y_test is None:
            return []

        result = []
        y_test = series_to_dataframe(self.y_test)
        if isinstance(y_test, pd.DataFrame):
            row = json.loads(y_test.iloc[0].to_json())
            cols = y_test.columns
            for y in cols:
                result.append({
                    'name': y,
                    'sample': row[str(y)],
                    'type': y_test[y].dtype.name
                })
        else:  # numpy array with multiple dimensions
            row = y_test[0]
            y = {
                'name': None,
                'sample': row.tolist(),
                'type': y_test.dtype.name
            }
            shape = normalize_shape(y_test.shape)
            if shape:
                y['shape'] = shape
            result.append(y)

        return result

    def outputs(self) -> list:
        return []

    def params(self) -> dict:
        if hasattr(self.model, 'get_params') and callable(self.model.get_params):
            return convert_to_json_format(self.model.get_params())
        return {}

    def save_model(self, model_path) -> 'ModelSerialization':
        serialization = self.serialization()
        if serialization == ModelSerialization.JOBLIB:
            try:
                import joblib
            except ImportError:
                from sklearn.externals import joblib
            joblib.dump(self.model, model_path)
        elif serialization == ModelSerialization.PICKLE:
            import pickle
            with open(model_path, 'wb') as f:
                pickle.dump(self.model, f)
        return serialization

    def model_metadata(self, as_json=False, **kwargs) -> dict:
        """Get the model metadata.
        :return: A dict contains model metadata
        """
        if self.model_type() == 'Spark' and not self.is_pipeline_model():
            raise ValueError(f'The Spark model should be a PipelineModel, {self.algorithm()} was given')

        # get the source code of an input object
        object_name = None
        object_source = None
        if self.source_object is not None:
            try:
                import inspect
                object_name = self.source_object.__name__
                object_source = inspect.getsource(self.source_object)
            except Exception as ex:
                logging.warning(f'An error occurred when inspecting the source object "({ex})" {traceback.format_exc()}')
                pass

        result = {
            'runtime': self.runtime(),
            'type': self.model_type(),
            'framework': self.framework(),
            'framework_version': self.framework_version(),
            'function_name': self.function_name(),
            'serialization': self.serialization(),
            'algorithm': self.algorithm(),
            'metrics': self.evaluate_metrics(),
            'inputs': self.inputs(),
            'targets': self.targets(),
            'outputs': self.outputs(),
            'object_source': object_source,
            'object_name': object_name,
            'params': self.params()
        }

        if as_json:
            result = json.dumps(result, indent=kwargs.get('indent'))
        return result

    def evaluate_metrics_by_sklearn(self, x_test, y_test, function_name) -> dict:
        if x_test is None or y_test is None:
            return {}

        try:
            # convert to numpy array if they are not
            x_test = to_ndarray(x_test)
            y_test = to_ndarray(y_test)

            shape = y_test.shape
            if len(shape) > 1 and shape[1] > 1:
                y_test = np.argmax(y_test, axis=1)

            if function_name == MiningFunction.CLASSIFICATION:
                from sklearn.metrics import accuracy_score
                y_pred = self.predict(x_test)
                accuracy = accuracy_score(y_test, y_pred)
                return {
                    'accuracy': accuracy
                }
            elif function_name == MiningFunction.REGRESSION:
                from sklearn.metrics import explained_variance_score
                y_pred = self.predict(x_test)
                explained_variance = explained_variance_score(y_test, y_pred)
                return {
                    'explained_variance': explained_variance
                }
            else:
                return {}
        except Exception as ex:
            logging.warning(
                f'An error occurred when evaluating the model performance metric ("{ex}") {traceback.format_exc()}')
            return {}

