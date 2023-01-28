import itertools
from pathlib import Path
from typing import Dict, Union

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.metrics import (
    average_precision_score,
    confusion_matrix,
    f1_score,
    make_scorer,
    precision_recall_curve,
    precision_score,
    recall_score,
)
from sklearn.model_selection import StratifiedKFold, cross_val_predict, cross_val_score

from fraud_analysis.config.core import OUTPUTS_DIR, config


def plot_confusion_matrix(
    cm,
    classes,
    out_path,
    normalize=False,
    title="Confusion matrix",
    cmap=plt.cm.Oranges,
):
    """
    This function prints and plots the confusion matrix.
    Normalization can be applied by setting `normalize=True`.
    """
    if normalize:
        cm = cm.astype("float") / cm.sum(axis=1)[:, np.newaxis]

    plt.figure(figsize=(10, 10))
    plt.imshow(cm, interpolation="nearest", cmap=cmap)
    plt.title(title, size=24)
    plt.colorbar(aspect=4)
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=45, size=14)
    plt.yticks(tick_marks, classes, size=14)

    fmt = ".2f" if normalize else "d"
    thresh = cm.max() / 2.0

    # Labeling the plot
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(
            j,
            i,
            format(cm[i, j], fmt),
            fontsize=20,
            horizontalalignment="center",
            color="white" if cm[i, j] > thresh else "black",
        )

    plt.grid(None)
    plt.tight_layout()
    plt.ylabel("True label", size=18)
    plt.xlabel("Predicted label", size=18)

    # Save
    plt.savefig(out_path, dpi=300, bbox_inches="tight")


def plot_multiclass_prc(
    y_val: pd.Series,
    y_scores: pd.Series,
    mapping: Dict,
    out_path: Union[str, Path],
    figsize: tuple[int, int] = (15, 8),
):
    """plot_multiclass_prc

    Args:
        y_val (pd.Series): true values of DV
        y_scores (pd.Series): probability
        estimation of DV
        mapping (Dict): mapping dictionary of
        numeric encoding of DV to its string encoding
        out_path (Union[str, Path]): output
        path of the saved PRC png figure
        figsize (tuple[int, int], optional): Size of
        PRC figure. Defaults to (15, 8).
    """

    # structures
    precisions = dict()
    recalls = dict()
    auprcs = dict()

    # get dummy variables for y_val, one for each level
    y_val_dummies = pd.get_dummies(y_val, drop_first=False).values

    # Compute precision, recall for each class
    # Also compute the AUPRC for each class
    for k, v in mapping.items():
        precisions[v], recalls[v], _ = precision_recall_curve(
            y_val_dummies[:, k - 1], y_scores[:, k - 1]
        )
        auprcs[v] = average_precision_score(y_val_dummies[:, k - 1], y_scores[:, k - 1])

    # plot precision and recall vs threshold for each class
    fig, ax = plt.subplots(figsize=figsize)
    plt.style.use("fivethirtyeight")
    plt.rcParams["font.size"] = 12

    for k, v in mapping.items():
        ax.plot(
            recalls[v],
            precisions[v],
            label=f"PRC for class {v} (area = {round(auprcs[v],2)}"
            + f" vs prop of class: {round(y_val_dummies[:, k - 1].mean(),2)})",
        )
    # Plot settings
    ax.set_xlim([0.0, 1.0])  # set x and y limits
    ax.set_ylim([0.0, 1.05])

    ax.set_xlabel("Recall")  # set x and y labels and title
    ax.set_ylabel("Precision")
    ax.set_title("Precision and Recall Curves")

    ax.legend(loc="best")
    # plt.show()
    plt.savefig(out_path, dpi=300, bbox_inches="tight")


def evaluate(pipeline, X_train, y_train):
    # Init the StratifiedKFold object
    skf = StratifiedKFold(
        n_splits=config.model_config.NFOLDS,
        shuffle=True,
        random_state=config.model_config.RANDOM_STATE,
    )
    match config.model_config.SCORING:
        case "f1_macro":
            scorer = make_scorer(f1_score, average="macro")
        case "precision_macro":
            scorer = make_scorer(precision_score, average="macro")
        case "recall_macro":
            scorer = make_scorer(recall_score, average="macro")
        case _:
            scorer = make_scorer(f1_score, average="macro")

    # Score the pipeline with CV (estimated test
    # scores for f1_score, precision, or recall)
    cv_scores = cross_val_score(
        estimator=pipeline, X=X_train, y=y_train, cv=skf, scoring=scorer
    )

    print(
        f"The mean cv score (macro {config.model_config.SCORING} score)"
        + f"is {round(np.mean(cv_scores),2)} with standard"
        + f" deviation of {round(np.std(cv_scores),2)}."
    )

    # Plot confusion martrix and prc

    # Compute clean y_train estimated probabilities
    y_train_pred_scores = cross_val_predict(
        estimator=pipeline, X=X_train, y=y_train, cv=skf, method="predict_proba"
    )

    # Compute clean y_train predictions
    y_train_pred = cross_val_predict(
        estimator=pipeline, X=X_train, y=y_train, cv=skf, method="predict"
    )

    # Plot confusion matrix
    cm = confusion_matrix(y_train, y_train_pred)
    plot_confusion_matrix(
        cm=cm,
        classes=["Not Fraud", "Fraud"],
        out_path=Path(OUTPUTS_DIR, "confusion_matrix_CV.png"),
        normalize=False,
        title="Fraud Detection Confusion Matrix from CV",
    )

    # Plot PRC curve
    plot_multiclass_prc(
        y_val=y_train,
        y_scores=y_train_pred_scores,
        mapping={1: "No Fraud", 2: "Fraud"},
        out_path=Path(OUTPUTS_DIR, "prc_CV.png"),
    )


def evaluate_on_test_set(y_test, y_pred, y_pred_scores, save_dir=None):
    """evaluate_on_test_set
    Given y_test and predictions of X_test using the trained pipeline,
    generate confusion matrix and PRC

    Args:
        y_test (pd.DataFrame): response variable of the test set
        y_pred (pd.Series): predictions from X_test using the trained pipeline
        y_pred_scores (np.ndarray): predicted probabilities of fraud (positive class)
        from X_test using the trained pipeline
        save_dir: user specified Path for saving evaluation figures
    """
    # If no user-specified output paths 
    # for the confusion matrix and PRC 
    # figures are provided
    if save_dir is None:
        save_dir = OUTPUTS_DIR
    
    cm = confusion_matrix(y_test, y_pred)
    plot_confusion_matrix(
        cm=cm,
        classes=["Not Fraud", "Fraud"],
        out_path=Path(save_dir, "confusion_matrix_test_set.png"),
        normalize=False,
        title="Fraud Detection Confusion Matrix on the Test Set",
    )

    # Plot PRC curve
    plot_multiclass_prc(
        y_val=y_test.iloc[:, 0],  # need to turn dataframe to series
        y_scores=y_pred_scores,
        mapping={1: "No Fraud", 2: "Fraud"},
        out_path=Path(save_dir, "prc_test_set.png"),
    )


def plot_feature_importance(data_pipeline, X_train, out_path, top_n=None):

    # features dropped due to nzv
    dropped_features = data_pipeline.named_steps.drop_nzv.features_to_drop_

    # get features that remained after dropping those with nzv
    selected_features = [f for f in X_train.columns.values if f not in dropped_features]

    # if no top_n is provided, get all features
    if top_n is None:
        top_n = len(selected_features)

    # Get fitted Random Forest model
    fitted_rf = data_pipeline.named_steps["clf"]

    # Get feature importances and put into a dataframe
    feature_results = pd.DataFrame(
        {"feature": selected_features, "importance": fitted_rf.feature_importances_}
    )

    # Plot feature importance

    # Plot styling
    plt.style.use("fivethirtyeight")
    plt.rcParams["font.size"] = 12

    fig = plt.figure(figsize=(10, 5))
    ax = fig.add_subplot(1, 1, 1)

    (
        feature_results.sort_values("importance", ascending=False)
        .set_index("feature")
        .head(top_n)
        .plot.barh(
            ax=ax,
            color="k",
            alpha=0.7,
            title=f"Top {top_n} important features from random forest",
            ylabel="Normalized feature importance",
            xlabel="Features",
        )
    )
    plt.savefig(out_path, dpi=300, bbox_inches="tight")
