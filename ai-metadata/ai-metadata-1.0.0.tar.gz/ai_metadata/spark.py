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
import logging
import traceback
from .base import MetadataModel, MiningFunction, ModelSerialization
from .utils import extract_major_minor_version


class SparkModel(MetadataModel):
    """A wrapper of a Spark mllib model
    """

    @staticmethod
    def is_support(model) -> bool:
        try:
            from pyspark.ml import Model
            return isinstance(model, Model)
        except ImportError:
            return False

    def is_pipeline_model(self):
        try:
            from pyspark.ml import PipelineModel
            return isinstance(self.model, PipelineModel)
        except ImportError:
            return False

    def model_type(self):
        return 'mllib'

    def framework(self) -> str:
        return 'Spark'

    def framework_version(self) -> str:
        from pyspark import SparkConf, SparkContext
        sc = SparkContext.getOrCreate(conf=SparkConf())
        return extract_major_minor_version(sc.version)

    def function_name(self) -> 'MiningFunction':
        return super().function_name()

    def serialization(self) -> 'ModelSerialization':
        return ModelSerialization.SPARK

    def function_name(self) -> 'MiningFunction':
        from pyspark.ml import PipelineModel
        if isinstance(self.model, PipelineModel):
            stages = self.model.stages
            for x in reversed(stages):
                typ = self._infer_mining_function_by_model_type(x)
                if typ is not None:
                    return typ
        else:
            typ = self._infer_mining_function_by_model_type(self.model)
            if typ is not None:
                return typ
        return MiningFunction.UNKNOWN

    def predict(self, data):
        prediction_col = self._get_prediction_col()
        prediction = self.predict_raw(data)
        return prediction[prediction_col]

    def predict_proba(self, data):
        probability_col = self._get_probability_col()
        if probability_col is not None:
            return self.predict_raw(data)[probability_col]
        super().predict_proba(data)

    def predict_raw(self, data, **kwargs):
        return self.model.transform(data)

    def evaluate_metrics(self) -> dict:
        if self.data_test is None:
            return {}

        try:
            prediction = self.model.transform(self.data_test)
            label_col = self._get_label_col()
            predict_col = self._get_prediction_col()
            function_name = self.function_name()
            if function_name == MiningFunction.CLASSIFICATION:
                accuracy = prediction.rdd.filter(
                    lambda x: x[label_col] == x[predict_col]).count() * 1.0 / prediction.count()
                return {
                    'accuracy': accuracy
                }
            elif function_name == MiningFunction.REGRESSION:
                numerator = prediction.rdd.map(lambda x: x[label_col] - x[predict_col]).variance()
                denominator = prediction.rdd.map(lambda x: x[label_col]).variance()
                explained_variance = 1.0 - numerator / denominator
                return {
                    'explainedVariance': explained_variance
                }
            else:
                return {}
        except Exception as ex:
            logging.warning(
                f'An error occurred when evaluating the Spark model performance metric ("{ex}") {traceback.format_exc()}')
            return {}

    def inputs(self) -> list:
        if self.data_test is None:
            return []

        row = json.loads(self.data_test.limit(1).toPandas().iloc[0].to_json())
        label_col = self._get_label_col()
        cols = row.keys()
        result = []
        for x in cols:
            if x != label_col:
                result.append(({
                    'name': x,
                    'sample': row[x],
                    'type': type(row[x]).__name__
                }))
        return result

    def targets(self) -> list:
        if self.data_test is None:
            return []

        row = json.loads(self.data_test.limit(1).toPandas().iloc[0].to_json())
        label_col = self._get_label_col()
        cols = row.keys()
        result = []
        for x in cols:
            if x == label_col:
                result.append(({
                    'name': x,
                    'sample': row[x],
                    'type': type(row[x]).__name__
                }))
        return result

    def params(self) -> dict:
        from pyspark.ml import PipelineModel
        if isinstance(self.model, PipelineModel):
            result = {}
            for x in self.model.stages:
                result[x.uid] = {param.name: value for param, value in x.extractParamMap().items()}
            return result
        else:
            return {param.name: value for param, value in self.model.extractParamMap().items()}

    def save_model(self, model_path) -> 'ModelSerialization':
        self.model.write().overwrite().save(model_path)
        return self.serialization()

    def _get_label_col(self):
        from pyspark.ml import PipelineModel
        from pyspark.ml.param.shared import HasLabelCol, HasOutputCol, HasInputCol

        if isinstance(self.model, PipelineModel):
            stages = self.model.stages
            label_col = None
            for i, x in enumerate(reversed(stages)):
                if isinstance(x, HasLabelCol):
                    label_col = x.getLabelCol()
                    break

            # find the first input column
            reversed_stages = stages[:]
            reversed_stages.reverse()
            for x in reversed_stages[i + 1:]:
                if isinstance(x, HasOutputCol) and isinstance(x, HasInputCol) and x.getOutputCol() == label_col:
                    label_col = x.getInputCol()

            return 'label' if label_col is None else label_col
        else:
            return self.model.getLabelCol() if isinstance(self.model, HasLabelCol) else 'label'

    def _get_prediction_col(self):
        from pyspark.ml import PipelineModel
        from pyspark.ml.param.shared import HasPredictionCol
        if isinstance(self.model, PipelineModel):
            stages = self.model.stages
            for x in reversed(stages):
                if isinstance(x, HasPredictionCol):
                    return x.getPredictionCol()
        elif isinstance(self.model, HasPredictionCol):
            return self.model.getPredictionCol()
        return 'prediction'

    def _get_probability_col(self):
        from pyspark.ml import PipelineModel
        from pyspark.ml.param.shared import HasProbabilityCol
        if isinstance(self.model, PipelineModel):
            stages = self.model.stages
            for x in reversed(stages):
                if isinstance(x, HasProbabilityCol):
                    return x.getProbabilityCol()
        elif isinstance(self.model, HasProbabilityCol):
            return self.model.getProbabilityCol()
        return None

    @staticmethod
    def _infer_mining_function_by_model_type(model):
        from pyspark.ml.classification import ClassificationModel
        from pyspark.ml.regression import RegressionModel
        from pyspark.ml.clustering import KMeansModel, GaussianMixtureModel, BisectingKMeansModel, LDAModel
        if isinstance(model, ClassificationModel):
            return MiningFunction.CLASSIFICATION
        if isinstance(model, RegressionModel):
            return MiningFunction.REGRESSION
        if isinstance(model, (KMeansModel, GaussianMixtureModel, BisectingKMeansModel, LDAModel)):
            return MiningFunction.CLUSTERING
        return None

