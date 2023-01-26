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

import pytest

from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from ai_metadata import MetadataModel, MiningFunction, ModelSerialization

seed = 123456


def test_classification():
    X, y = datasets.load_iris(return_X_y=True, as_frame=True)
    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=seed)
    svc = SVC(probability=True, random_state=seed)
    svc.fit(X_train, y_train)

    model = MetadataModel.wrap(svc,
                               x_test=X_test,
                               y_test=y_test)
    model_metadata = model.model_metadata()
    print(model.model_metadata(as_json=True, indent=4))

    assert model_metadata['function_name'] == MiningFunction.CLASSIFICATION
    assert model_metadata['serialization'] in (ModelSerialization.JOBLIB, ModelSerialization.PICKLE)
    assert model_metadata['metrics'] != {}
    assert model_metadata['inputs'] == [
        {
            "name": "sepal length (cm)",
            "sample": 5.7,
            "type": "float64"
        },
        {
            "name": "sepal width (cm)",
            "sample": 4.4,
            "type": "float64"
        },
        {
            "name": "petal length (cm)",
            "sample": 1.5,
            "type": "float64"
        },
        {
            "name": "petal width (cm)",
            "sample": 0.4,
            "type": "float64"
        }
    ]
    assert model_metadata['targets'] == [
        {
            "name": "target",
            "sample": 0,
            "type": "int64"
        }
    ]
    assert model.predict([[x['sample'] for x in model_metadata['inputs']]]).tolist()
    assert model.predict_proba([[x['sample'] for x in model_metadata['inputs']]]).tolist()
    assert model.save_model('./sklearn-cls-numpy')


def test_classification_pipeline():
    from sklearn.pipeline import Pipeline
    from sklearn.tree import DecisionTreeClassifier
    from sklearn.preprocessing import StandardScaler

    X, y = datasets.load_iris(return_X_y=True, as_frame=True)
    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=seed)

    pipeline = Pipeline([
        ("scaler", StandardScaler()),
        ("model", DecisionTreeClassifier(random_state=seed))
    ])
    pipeline.fit(X_train, y_train)

    model = MetadataModel.wrap(pipeline,
                               x_test=X_test,
                               y_test=y_test)
    model_metadata = model.model_metadata()
    print(model.model_metadata(as_json=True, indent=4))

    assert model_metadata['function_name'] == MiningFunction.CLASSIFICATION
    assert model_metadata['metrics'] != {}
    assert model_metadata['inputs'] == [
        {
            "name": "sepal length (cm)",
            "sample": 5.7,
            "type": "float64"
        },
        {
            "name": "sepal width (cm)",
            "sample": 4.4,
            "type": "float64"
        },
        {
            "name": "petal length (cm)",
            "sample": 1.5,
            "type": "float64"
        },
        {
            "name": "petal width (cm)",
            "sample": 0.4,
            "type": "float64"
        }
    ]
    assert model_metadata['targets'] == [
        {
            "name": "target",
            "sample": 0,
            "type": "int64"
        }
    ]
    assert model.predict([[x['sample'] for x in model_metadata['inputs']]]).tolist()
    assert model.predict_proba([[x['sample'] for x in model_metadata['inputs']]]).tolist()
    assert model.is_pipeline_model()
    assert model.save_model('./sklearn-cls-pipeline')


def test_classification_without_test_data():
    # X, y are ndarray without columns
    X, y = datasets.load_iris(return_X_y=True)
    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=seed)
    svc = SVC(probability=True, random_state=seed)
    svc.fit(X_train, y_train)

    model = MetadataModel.wrap(svc)
    model_metadata = model.model_metadata()
    print(model.model_metadata(as_json=True, indent=4))

    assert model_metadata['function_name'] == MiningFunction.CLASSIFICATION
    assert model_metadata['serialization'] in (ModelSerialization.JOBLIB, ModelSerialization.PICKLE)
    assert model_metadata['metrics'] == {}
    assert model_metadata['inputs'] == [
        {
            "name": None,
            "type": "numeric",
            "shape": [
                None,
                4
            ]
        }
    ]
    assert model_metadata['targets'] == [
        {
            "name": None,
            "type": "numeric"
        }
    ]
    assert model.save_model('./sklearn-cls')


def test_regression():
    from sklearn.linear_model import LinearRegression

    X, y = datasets.load_boston(return_X_y=True)
    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=seed)

    linear = LinearRegression()
    linear.fit(X_train, y_train)

    model = MetadataModel.wrap(linear,
                               x_test=X_test,
                               y_test=y_test)
    model_metadata = model.model_metadata()
    print(model.model_metadata(as_json=True, indent=4))

    assert model_metadata['function_name'] == MiningFunction.REGRESSION
    assert model_metadata['serialization'] in (ModelSerialization.JOBLIB, ModelSerialization.PICKLE)
    assert model_metadata['metrics'] != {}
    assert model_metadata['inputs'] == [
        {
            "name": None,
            "sample": [
                [
                    22.5971,
                    0.0,
                    18.1,
                    0.0,
                    0.7,
                    5.0,
                    89.5,
                    1.5184,
                    24.0,
                    666.0,
                    20.2,
                    396.9,
                    31.99
                ]
            ],
            "type": "float64",
            "shape": [
                None,
                13
            ]
        }
    ]
    assert model_metadata['targets'] == [
        {
            "name": None,
            "sample": 7.4,
            "type": "float64"
        }
    ]
    assert model.predict(model_metadata['inputs'][0]["sample"]).tolist()
    with pytest.raises(AttributeError):
        model.predict_proba(model_metadata['inputs'][0]["sample"])
    assert model.save_model('./sklearn-reg')


def test_clustering():
    from sklearn.cluster import KMeans

    X, y = datasets.load_iris(return_X_y=True)
    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=seed)
    kmeans = KMeans(n_clusters=3, random_state=seed).fit(X_train)

    model = MetadataModel.wrap(kmeans,
                               x_test=X_test,
                               source_object=test_clustering)
    model_metadata = model.model_metadata()
    print(model.model_metadata(as_json=True, indent=4))

    assert model_metadata['function_name'] == MiningFunction.CLUSTERING
    assert model_metadata['object_name'] == 'test_clustering'
    assert model_metadata['object_source']
    assert model_metadata['metrics'] == {}
    assert model.predict(model_metadata['inputs'][0]["sample"]).tolist()
    assert model.save_model('./sklearn-clustering')

