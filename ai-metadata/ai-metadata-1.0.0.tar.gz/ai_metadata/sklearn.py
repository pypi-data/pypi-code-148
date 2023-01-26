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

from .base import MetadataModel, MiningFunction, ModelSerialization
from .utils import extract_major_minor_version


class SKLearnModel(MetadataModel):
    """A wrapper of a scikit learn model
    """

    @staticmethod
    def is_support(model) -> bool:
        try:
            from sklearn.base import BaseEstimator
            return isinstance(model, BaseEstimator)
        except ImportError:
            return False

    def is_sklearn_format(self) -> bool:
        return True

    def is_pipeline_model(self) -> bool:
        from sklearn.pipeline import Pipeline
        return isinstance(self.model, Pipeline)

    def framework(self) -> str:
        return 'Scikit-learn'

    def framework_version(self) -> str:
        import sklearn
        return extract_major_minor_version(sklearn.__version__)

    def serialization(self) -> 'ModelSerialization':
        try:
            import joblib
        except ImportError:
            try:
                from sklearn.externals import joblib
            except ImportError:
                return ModelSerialization.PICKLE
        return ModelSerialization.JOBLIB

    def function_name(self) -> 'MiningFunction':
        from sklearn.base import is_classifier, is_regressor
        if is_classifier(self.model):
            return MiningFunction.CLASSIFICATION
        if is_regressor(self.model):
            return MiningFunction.REGRESSION
        if getattr(self.model, "_estimator_type", None) == "clusterer":
            return MiningFunction.CLUSTERING
        return super().function_name()

    def predict_proba(self, data):
        if hasattr(self.model, 'predict_proba'):
            return self.model.predict_proba(data)
        super().predict_proba(data)

    def inputs(self) -> list:
        result = super().inputs()
        if not result:
            if hasattr(self.model, 'feature_names_in_'):
                cols = self.model.feature_names_in_
                for x in cols:
                    result.append({
                        'name': x,
                        'type': 'numeric'
                    })
            elif hasattr(self.model, 'n_features_in_'):
                result.append({
                    'name': None,
                    'type': 'numeric',
                    'shape': [None, self.model.n_features_in_]
                })
        return result

    def targets(self) -> list:
        result = super().targets()
        if not result:
            result.append({
                'name': None,
                'type': 'numeric'
            })
        return result

