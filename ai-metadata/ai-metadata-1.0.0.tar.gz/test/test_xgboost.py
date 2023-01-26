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
test_size = 0.33


def test_classification():
    from xgboost import XGBClassifier

    X, y = datasets.load_iris(return_X_y=True, as_frame=True)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=seed)

    classifier = XGBClassifier(max_depth=3, objective='multi:softprob')
    classifier = classifier.fit(X_train, y_train)

    model = MetadataModel.wrap(classifier,
                               x_test=X_test,
                               y_test=y_test)
    model_metadata = model.model_metadata()

    print(model.model_metadata(as_json=True, indent=4))
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
    assert model_metadata['serialization'] == ModelSerialization.JOBLIB
    assert model.save_model('./xgboost-cls')


def test_regression():
    from xgboost import XGBRegressor

    X, y = datasets.load_boston(return_X_y=True)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=seed)

    regressor = XGBRegressor(objective='reg:linear',
                             colsample_bytree=0.3,
                             learning_rate=0.1,
                             max_depth=5,
                             alpha=10,
                             n_estimators=10,
                             seed=seed)
    regressor.fit(X_train, y_train)

    model = MetadataModel.wrap(regressor,
                               x_test=X_test,
                               y_test=y_test)
    model_metadata = model.model_metadata()

    print(model.model_metadata(as_json=True, indent=4))
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
    assert model_metadata['serialization'] == ModelSerialization.JOBLIB
    assert model.save_model('./xgboost-reg')


def test_raw_classification():
    import xgboost as xgb

    X, y = datasets.load_iris(return_X_y=True, as_frame=True)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=seed)

    dtrain = xgb.DMatrix(X_train, label=y_train)
    dtest = xgb.DMatrix(X_test, label=y_test)
    param = {
        'max_depth': 3,
        'eta': 0.3,
        'objective': 'multi:softprob',
        'num_class': 3}

    booster = xgb.train(param, dtrain)

    model = MetadataModel.wrap(booster,
                               x_test=X_test,
                               y_test=y_test)
    model_metadata = model.model_metadata()

    print(model.model_metadata(as_json=True, indent=4))
    prediction = model.predict([[x['sample'] for x in model_metadata['inputs']]])
    proba = model.predict_proba([[x['sample'] for x in model_metadata['inputs']]])
    print(f"prediction: {prediction.tolist()}")
    print(f"proba: {proba.tolist()}")
    assert model_metadata['function_name'] == MiningFunction.CLASSIFICATION
    assert model_metadata['serialization'] == ModelSerialization.XGBOOST
    assert model_metadata['algorithm'] == 'Booster'
    assert model_metadata['metrics'] != {}

    model = MetadataModel.wrap(booster)
    model_metadata_no_test_data = model.model_metadata()

    print(model.model_metadata(as_json=True, indent=4))
    assert model_metadata_no_test_data['function_name'] == MiningFunction.CLASSIFICATION
    assert model_metadata_no_test_data['serialization'] == ModelSerialization.XGBOOST
    assert model_metadata_no_test_data['metrics'] == {}

    assert model.save_model('./xgboost-raw-cls.json')
    assert model.save_model('./xgboost-raw-cls.ubj')


def test_raw_regression():
    import xgboost as xgb

    X, y = datasets.load_boston(return_X_y=True)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=seed)

    dtrain = xgb.DMatrix(X_train, y_train)
    dtest = xgb.DMatrix(X_test)
    params = {'eta': 0.1,
              'seed': 0,
              'subsample': 0.8,
              'colsample_bytree': 0.8,
              'objective': 'reg:linear',
              'max_depth': 3,
              'min_child_weight': 1}

    booster = xgb.train(params, dtrain)

    model = MetadataModel.wrap(booster,
                               x_test=X_test,
                               y_test=y_test)
    model_metadata = model.model_metadata()

    print("With test data: " + model.model_metadata(as_json=True, indent=4))
    prediction = model.predict(model_metadata['inputs'][0]['sample'])
    print(f"prediction: {prediction.tolist()}")
    with pytest.raises(AttributeError):
        model.predict_proba(model_metadata['inputs'][0]['sample'])
    assert model_metadata['function_name'] == MiningFunction.REGRESSION
    assert model_metadata['serialization'] == ModelSerialization.XGBOOST
    assert model_metadata['algorithm'] == 'Booster'
    assert model_metadata['metrics'] != {}

    model = MetadataModel.wrap(booster)
    model_metadata_no_test_data = model.model_metadata()
    print("Without test data: " + model.model_metadata(as_json=True, indent=4))
    assert model_metadata_no_test_data['function_name'] == MiningFunction.REGRESSION
    assert model_metadata_no_test_data['serialization'] == ModelSerialization.XGBOOST
    assert model_metadata_no_test_data['metrics'] == {}
    assert model.save_model('./xgboost-raw-cls.json')
    assert model.save_model('./xgboost-raw-cls.ubj')

