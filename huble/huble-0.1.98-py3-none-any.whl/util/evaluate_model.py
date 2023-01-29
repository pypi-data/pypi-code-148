import pandas as pd
import sklearn
from huble.sklearn.metrics import log_metrics, upload

def evaluate_model(model, test_dataset, target_column, task_type):
    y_test = test_dataset[target_column]
    X_test = test_dataset.drop([target_column], axis=1)
    y_pred = model.predict(X_test)
    metrics = log_metrics(y_test, y_pred, task_type)
    upload(metrics)
    return metrics
