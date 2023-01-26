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
from sklearn import datasets
from ai_metadata import MetadataModel, ModelSerialization, MiningFunction

seed = 123456
test_size = 0.25


def test_classification():
    from pyspark.sql import SparkSession
    from pyspark.ml.classification import LogisticRegression
    from pyspark.ml.feature import VectorAssembler
    from pyspark.ml import Pipeline

    iris = datasets.load_iris(as_frame=True)

    spark = SparkSession.builder.getOrCreate()
    df = spark.createDataFrame(iris.frame)
    df.show()

    df_train, df_test = df.randomSplit([1.0 - test_size, test_size], seed)
    assembler = VectorAssembler(inputCols=iris.feature_names,
                                outputCol='features')

    lr = LogisticRegression().setLabelCol(iris.target.name)
    pipeline = Pipeline(stages=[assembler, lr])
    pipeline_model = pipeline.fit(df_train)

    model = MetadataModel.wrap(pipeline_model,
                               data_test=df_test)
    model_metadata = model.model_metadata()

    print(model.model_metadata(as_json=True, indent=4))
    assert model_metadata['serialization'] == ModelSerialization.SPARK
    assert model_metadata['function_name'] == MiningFunction.CLASSIFICATION
    assert model.save_model('./spark-cls')


def test_regression():
    from pyspark.sql import SparkSession
    from pyspark.ml.regression import LinearRegression
    from pyspark.ml.feature import VectorAssembler
    from pyspark.ml import Pipeline

    boston = datasets.load_boston()
    target_name = 'MEDV'
    boston_df = pd.DataFrame(boston.data, columns=boston.feature_names)
    boston_df[target_name] = boston.target

    spark = SparkSession.builder.getOrCreate()
    df = spark.createDataFrame(boston_df)
    df.show()

    df_train, df_test = df.randomSplit([1.0 - test_size, test_size], seed=seed)
    assembler = VectorAssembler(inputCols=boston.feature_names, outputCol='features')

    lr = LinearRegression().setLabelCol(target_name)
    pipe = Pipeline(stages=[assembler, lr])
    pipeline_model = pipe.fit(df_train)

    model = MetadataModel.wrap(pipeline_model,
                               data_test=df_test)
    model_metadata = model.model_metadata()

    print(model.model_metadata(as_json=True, indent=4))
    assert model_metadata['serialization'] == ModelSerialization.SPARK
    assert model_metadata['function_name'] == MiningFunction.REGRESSION
    assert model.save_model('./spark-reg')

