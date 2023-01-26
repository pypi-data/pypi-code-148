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
from sklearn.model_selection import train_test_split
from sklearn import datasets
from ai_metadata import MetadataModel, ModelSerialization, MiningFunction

seed = 123456


def test_classification():
    from nyoka import skl_to_pmml
    from sklearn.pipeline import Pipeline
    from sklearn.tree import DecisionTreeClassifier
    from sklearn.preprocessing import StandardScaler

    X, y = datasets.load_iris(return_X_y=True, as_frame=True)
    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=seed)

    pipeline = Pipeline([
        ("scaler", StandardScaler()),
        ("model", DecisionTreeClassifier())
    ])
    pipeline.fit(X_train, y_train)

    # export the pipeline into PMML
    model_path = './pmml-cls.xml'
    skl_to_pmml(pipeline, X_train.columns, y_train.name, model_path)

    model = MetadataModel.wrap(model_path,
                               x_test=X_test,
                               y_test=y_test)
    model_metadata = model.model_metadata()
    print(model.model_metadata(as_json=True, indent=4))

    assert model_metadata['inputs'] == [
        {
            "name": "sepal length (cm)",
            "sample": 5.7,
            "type": "double"
        },
        {
            "name": "sepal width (cm)",
            "sample": 4.4,
            "type": "double"
        },
        {
            "name": "petal length (cm)",
            "sample": 1.5,
            "type": "double"
        },
        {
            "name": "petal width (cm)",
            "sample": 0.4,
            "type": "double"
        }
    ]
    assert model_metadata['targets'] == [
        {
            "name": "target",
            "sample": 0,
            "type": "integer"
        }
    ]
    assert model_metadata['outputs'] == [
        {
            "name": "probability_0",
            "type": "double"
        },
        {
            "name": "probability_1",
            "type": "double"
        },
        {
            "name": "probability_2",
            "type": "double"
        },
        {
            "name": "predicted_target",
            "type": "integer"
        }
    ]

    prediction = model.predict({x['name']: x['sample'] for x in model_metadata['inputs']})
    assert prediction == 0
    proba = model.predict_proba({x['name']: x['sample'] for x in model_metadata['inputs']})
    assert proba == {'probability_0': 1.0, 'probability_1': 0.0, 'probability_2': 0.0}
    assert model_metadata['metrics']
    assert model_metadata['function_name'] == MiningFunction.CLASSIFICATION
    assert model_metadata['serialization'] == ModelSerialization.PMML
    assert model.save_model('./pmml-cls-saved.xml')


def test_regression():
    from nyoka import skl_to_pmml
    from sklearn.pipeline import Pipeline
    from sklearn.tree import DecisionTreeRegressor

    boston = datasets.load_boston()
    X, y = boston.data, boston.target
    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=seed)

    pipeline_obj = Pipeline([
        ('model', DecisionTreeRegressor(random_state=seed))
    ])
    pipeline_obj.fit(X_train, y_train)

    # export the pipeline into PMML
    model_path = './pmml-reg.xml'
    skl_to_pmml(pipeline_obj, boston.feature_names, 'MEDV', model_path)
    with open(model_path) as f:
        model_content = f.read()

    model = MetadataModel.wrap(model_content,
                               x_test=X_test,
                               y_test=y_test)
    model_metadata = model.model_metadata()
    print(model.model_metadata(as_json=True, indent=4))

    assert model_metadata['inputs'] == [
        {
            "name": "CRIM",
            "sample": 22.5971,
            "type": "double"
        },
        {
            "name": "ZN",
            "sample": 0.0,
            "type": "double"
        },
        {
            "name": "INDUS",
            "sample": 18.1,
            "type": "double"
        },
        {
            "name": "CHAS",
            "sample": 0.0,
            "type": "double"
        },
        {
            "name": "NOX",
            "sample": 0.7,
            "type": "double"
        },
        {
            "name": "RM",
            "sample": 5.0,
            "type": "double"
        },
        {
            "name": "AGE",
            "sample": 89.5,
            "type": "double"
        },
        {
            "name": "DIS",
            "sample": 1.5184,
            "type": "double"
        },
        {
            "name": "RAD",
            "sample": 24.0,
            "type": "double"
        },
        {
            "name": "TAX",
            "sample": 666.0,
            "type": "double"
        },
        {
            "name": "PTRATIO",
            "sample": 20.2,
            "type": "double"
        },
        {
            "name": "B",
            "sample": 396.9,
            "type": "double"
        },
        {
            "name": "LSTAT",
            "sample": 31.99,
            "type": "double"
        }
    ]
    assert model_metadata['targets'] == [
        {
            "name": "MEDV",
            "sample": None,
            "type": "double"
        }
    ]
    assert model_metadata['outputs'] == [
        {
            "name": "predicted_MEDV",
            "type": "double"
        }
    ]
    prediction = model.predict({x['name']: x['sample'] for x in model_metadata['inputs']})
    assert prediction == 7.2
    with pytest.raises(AttributeError):
        model.predict_proba({x['name']: x['sample'] for x in model_metadata['inputs']})
    assert model_metadata['metrics']
    assert model_metadata['function_name'] == MiningFunction.REGRESSION
    assert model_metadata['serialization'] == ModelSerialization.PMML
    assert model.save_model('./pmml-reg-saved.xml')

