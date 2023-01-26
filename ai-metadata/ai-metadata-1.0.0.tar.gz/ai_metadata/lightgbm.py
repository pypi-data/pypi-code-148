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
from .base import MetadataModel, MiningFunction, ModelSerialization
from .utils import extract_major_minor_version, convert_to_json_format


class LightGBMModel(MetadataModel):
    """A wrapper of a LightGBM model
    """

    @staticmethod
    def is_support(model) -> bool:
        try:
            import lightgbm as lgb
            return isinstance(model, lgb.Booster) or \
                   isinstance(model, lgb.LGBMClassifier) or \
                   isinstance(model, lgb.LGBMRegressor)
        except ImportError:
            return False

    def is_sklearn_format(self):
        import lightgbm as lgb
        return isinstance(self.model, lgb.LGBMClassifier) or isinstance(self.model, lgb.LGBMRegressor)

    def framework(self) -> str:
        return 'LightGBM'

    def framework_version(self) -> str:
        import lightgbm as lgb
        return extract_major_minor_version(lgb.__version__)

    def serialization(self) -> 'ModelSerialization':
        return ModelSerialization.JOBLIB if self.is_sklearn_format() else ModelSerialization.LIGHTGBM

    def predict(self, data):
        if self.is_sklearn_format():
            return self.predict_raw(data)
        else:
            if self.function_name() == MiningFunction.CLASSIFICATION:
                return np.argmax(self.predict_raw(data), axis=1)
            else:
                return self.predict_raw(data)

    def predict_proba(self, data):
        import lightgbm as lgb

        if isinstance(self.model, lgb.LGBMClassifier):
            return self.model.predict_proba(data)
        elif self.function_name() == MiningFunction.CLASSIFICATION:
            return self.predict_raw(data)
        super().predict_proba(data)

    def function_name(self) -> 'MiningFunction':
        import lightgbm as lgb
        if isinstance(self.model, lgb.LGBMClassifier):
            return MiningFunction.CLASSIFICATION
        if isinstance(self.model, lgb.LGBMRegressor):
            return MiningFunction.REGRESSION

        result = super().function_name()
        if result == MiningFunction.UNKNOWN:
            params = self.params()
            objective = params.get('objective')
            if objective:
                if objective in ('binary', 'multiclass', 'multiclassova'):
                    result = MiningFunction.CLASSIFICATION
                else:
                    result = MiningFunction.REGRESSION
        return result

    def inputs(self) -> list:
        result = super().inputs()
        if not result:
            if hasattr(self.model, 'feature_name'):
                cols = self.model.feature_name()
                for x in cols:
                    result.append({
                        'name': x,
                        'type': 'numeric'
                    })
        return result

    def params(self) -> dict:
        result = super().params()
        if not result:
            if hasattr(self.model, 'params'):
                result = convert_to_json_format(self.model.params)
        return result

    def save_model(self, model_path) -> 'ModelSerialization':
        if self.serialization() == ModelSerialization.LIGHTGBM:
            self.model.save_model(model_path)
            return self.serialization()
        else:
            return super().save_model(model_path)

