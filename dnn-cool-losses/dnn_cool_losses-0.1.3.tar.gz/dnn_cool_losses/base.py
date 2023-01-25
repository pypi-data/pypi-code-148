import numpy as np
from dnn_cool_activations.base import sigmoid


def cross_entropy_on_logits(logits: np.ndarray, labels: np.ndarray, axis: int):
    logits = logits - logits.max(axis=axis, keepdims=True)
    e = np.exp(logits)
    s = np.sum(e, axis=axis)
    labels_expanded = np.expand_dims(labels, axis=axis)
    taken = np.take_along_axis(logits, labels_expanded, axis=axis)
    ces = np.log(s) - taken.squeeze(axis=axis)
    return ces


def cross_entropy_on_proba(proba: np.ndarray, labels: np.ndarray, axis: int, eps=1e-7):
    labels_expanded = np.expand_dims(labels, axis=axis)
    taken = np.take_along_axis(proba, labels_expanded, axis=axis)
    taken = np.clip(taken, eps, 1.0 - eps)
    ces = -np.log(taken).squeeze(axis)
    return ces


def binary_cross_entropy_on_proba(proba: np.ndarray, labels: np.ndarray, eps=1e-7):
    # Based on https://stackoverflow.com/a/67616451
    y_pred = np.clip(proba, eps, 1.0 - eps)
    term_0 = (1 - labels) * np.log(1.0 - y_pred + eps)
    term_1 = labels * np.log(y_pred + eps)
    return -(term_0 + term_1)


def binary_cross_entropy_on_logits(logits: np.ndarray, labels: np.ndarray):
    return binary_cross_entropy_on_proba(sigmoid(logits), labels)


def absolute_error(y_pred: np.ndarray, y_true: np.ndarray):
    return np.abs(y_pred - y_true)


def squared_error(y_pred: np.ndarray, y_true: np.ndarray):
    diff = y_pred - y_true
    return diff * diff
