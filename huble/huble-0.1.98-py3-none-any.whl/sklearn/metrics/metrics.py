import sklearn
import requests


def regression_metrics(y_true, y_pred):
    max_error = sklearn.metrics.max_error(y_true, y_pred)
    mean_absolute_error = sklearn.metrics.mean_absolute_error(y_true, y_pred)
    mean_squared_error = sklearn.metrics.mean_squared_error(y_true, y_pred)
    mean_squared_log_error = sklearn.metrics.mean_squared_log_error(y_true, y_pred)
    median_absolute_error = sklearn.metrics.median_absolute_error(y_true, y_pred)
    r2_score = sklearn.metrics.r2_score(y_true, y_pred)
    mean_poisson_deviance = sklearn.metrics.mean_poisson_deviance(y_true, y_pred)
    mean_gamma_deviance = sklearn.metrics.mean_gamma_deviance(y_true, y_pred)
    mean_tweedie_deviance = sklearn.metrics.mean_tweedie_deviance(y_true, y_pred)
    mean_pinball_loss = sklearn.metrics.mean_pinball_loss(y_true, y_pred)
    d2_absolute_error_score = sklearn.metrics.d2_absolute_error_score(y_true, y_pred)
    # create dictionary of metrics
    metrics = {
        "max_error": max_error,
        "mean_absolute_error": mean_absolute_error,
        "mean_squared_error": mean_squared_error,
        "mean_squared_log_error": mean_squared_log_error,
        "median_absolute_error": median_absolute_error,
        "r2_score": r2_score,
        "mean_poisson_deviance": mean_poisson_deviance,
        "mean_gamma_deviance": mean_gamma_deviance,
        "mean_tweedie_deviance": mean_tweedie_deviance,
        "mean_pinball_loss": mean_pinball_loss,
        "d2_absolute_error_score": d2_absolute_error_score,
    }
    return metrics


def classification_metrics(y_true, y_pred):
    accuracy_score = sklearn.metrics.accuracy_score(y_true, y_pred)
    balanced_accuracy_score = sklearn.metrics.balanced_accuracy_score(y_true, y_pred)
    cohen_kappa_score = sklearn.metrics.cohen_kappa_score(y_true, y_pred)
    f1_score = sklearn.metrics.f1_score(y_true, y_pred)
    fbeta_score = sklearn.metrics.fbeta_score(y_true, y_pred)
    hamming_loss = sklearn.metrics.hamming_loss(y_true, y_pred)
    jaccard_score = sklearn.metrics.jaccard_score(y_true, y_pred)
    log_loss = sklearn.metrics.log_loss(y_true, y_pred)
    matthews_corrcoef = sklearn.metrics.matthews_corrcoef(y_true, y_pred)
    precision_score = sklearn.metrics.precision_score(y_true, y_pred)
    recall_score = sklearn.metrics.recall_score(y_true, y_pred)
    zero_one_loss = sklearn.metrics.zero_one_loss(y_true, y_pred)
    # create dictionary of metrics
    metrics = {
        "accuracy_score": accuracy_score,
        "balanced_accuracy_score": balanced_accuracy_score,
        "cohen_kappa_score": cohen_kappa_score,
        "f1_score": f1_score,
        "fbeta_score": fbeta_score,
        "hamming_loss": hamming_loss,
        "jaccard_score": jaccard_score,
        "log_loss": log_loss,
        "matthews_corrcoef": matthews_corrcoef,
        "precision_score": precision_score,
        "recall_score": recall_score,
        "zero_one_loss": zero_one_loss,
    }
    return metrics


def log_metrics(y_true, y_pred, task):
    if task == "regression":
        metrics = regression_metrics(y_true, y_pred)
    elif task == "classification":
        metrics = classification_metrics(y_true, y_pred)
    return metrics


def upload_metrics(experiment_id, metrics):
    requests.put(f"http://localhost:8000/experiments/results/{experiment_id}", data=metrics)
