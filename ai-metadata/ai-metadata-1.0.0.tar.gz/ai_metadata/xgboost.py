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
from .utils import extract_major_minor_version


class XGBoostModel(MetadataModel):
    """A wrapper of a XGBoost model
    """

    @staticmethod
    def is_support(model) -> bool:
        try:
            import xgboost as xgb
            return isinstance(model, xgb.Booster) or \
                   isinstance(model, xgb.XGBClassifier) or \
                   isinstance(model, xgb.XGBRegressor)
        except ImportError:
            return False

    def is_sklearn_format(self):
        import xgboost as xgb
        return isinstance(self.model, xgb.XGBClassifier) or isinstance(self.model, xgb.XGBRegressor)

    def is_pipeline_model(self) -> bool:
        return False

    def framework(self) -> str:
        return 'XGBoost'

    def framework_version(self) -> str:
        import xgboost as xgb
        return extract_major_minor_version(xgb.__version__)

    def serialization(self) -> 'ModelSerialization':
        return ModelSerialization.JOBLIB if self.is_sklearn_format() else ModelSerialization.XGBOOST

    def predict(self, data):
        if self.is_sklearn_format():
            return self.predict_raw(data)
        else:
            data = self._prepare_data(data)
            if self.function_name() == MiningFunction.CLASSIFICATION:
                return np.argmax(self.predict_raw(data), axis=1)
            else:
                return self.model.predict(data)

    def predict_proba(self, data):
        import xgboost as xgb
        if isinstance(self.model, xgb.XGBClassifier):
            return self.model.predict_proba(data)
        elif self.function_name() == MiningFunction.CLASSIFICATION:
            data = self._prepare_data(data)
            return self.predict_raw(data)
        super().predict_proba(data)

    def function_name(self) -> 'MiningFunction':
        import xgboost as xgb
        if isinstance(self.model, xgb.XGBClassifier):
            return MiningFunction.CLASSIFICATION
        if isinstance(self.model, xgb.XGBRegressor):
            return MiningFunction.REGRESSION

        result = super().function_name()
        if result == MiningFunction.UNKNOWN:
            params = self.params()
            if 'learner' in params and 'learner_train_param' in params['learner']:
                objective = params['learner']['learner_train_param'].get('objective')
                if objective:
                    if objective.startswith('binary:') or objective.startswith('multi:'):
                        result = MiningFunction.CLASSIFICATION
                    else:
                        result = MiningFunction.REGRESSION
        return result

    def inputs(self) -> list:
        result = super().inputs()
        if not result:
            if hasattr(self.model, 'feature_names') and self.model.feature_names is not None \
                    and hasattr(self.model, 'feature_types') and self.model.feature_types is not None:
                for name, typ in zip(self.model.feature_names, self.model.feature_types):
                    result.append({
                        'name': name,
                        'type': typ
                    })
        return result

    def params(self) -> dict:
        result = super().params()
        if not result:
            if hasattr(self.model, 'save_config'):
                result = json.loads(self.model.save_config())
        return result

    def save_model(self, model_path) -> 'ModelSerialization':
        if self.serialization() == ModelSerialization.XGBOOST:
            self.model.save_model(model_path)
            return self.serialization()
        else:
            return super().save_model(model_path)

    def _prepare_data(self, data):
        import xgboost as xgb
        if not isinstance(data, xgb.DMatrix):
            feature_names = None
            if hasattr(self.model, 'feature_names') and self.model.feature_names is not None and \
                    not isinstance(data, pd.DataFrame):
                feature_names = self.model.feature_names
            data = xgb.DMatrix(data, feature_names=feature_names)
        return data

