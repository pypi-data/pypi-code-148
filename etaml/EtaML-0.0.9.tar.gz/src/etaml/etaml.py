#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Created on Apr 15 21:56 2021

Template for binary classifications of tabular data including preprocessing
# TODO: Silence dtreeviz "findfont" warning
# TODO: SHAP speedup (shap.sample(data, K) or shap.kmeans(data, K) to summarize the background as K samples)
# TODO: Handle NA imputation for categorical values
# TODO: Handle EDA visualizations (scaling!) for cases where there are categorical and/or missing values
# TODO: Add p values to performance bar plot indicating differences (Requires reuse of same fold for all classifiers)
# TODO: Runtime optimization by parallelizing folds
# TODO: Add quickload function to load all intermediate data and models for custom analysis
# TODO: Replace PDP plots with https://github.com/SauceCat/PDPbox
# TODO: Optional: Add EBM interpretability plots to XAI
# TODO: Add EBM surrogate interpretability plots to XAI
# TODO: Check how to make EBM work with calibration
# TODO: Check why some classifiers don't have the same number of measurements for the original models calibration curve
# TODO: Add Brier scores to output for calibration
# TODO: Add relevant output to log file in results
# TODO: Create config file parameters for dimensionality reduction techniques
# TODO: Base overall performance calculation on foldwise_predictions
# TODO: Save features that are removed during preprocessing (constant and missing ratio low) + add selection to inference
# TODO: Test MICE forest
# TODO: Make two output modi with more and less detailed output?
# TODO: Backtransform scaled features for interpretability methods
# TODO: Test multi class AUC
# TODO: For performance boxplot, add white square (mean) to legend
# TODO: Adapt system specifications in README, update installation instructions to include a venv
# TODO: Allow installation via pip
# TODO Add logging


Input data format specifications:
    - The file shall be a CSV file
    - The file shall have a header, containing the attribute names and the label name
    - The file shall have an index column containing a unique identifier for each instance

@author: cspielvogel
"""

import os
import json
import configparser
import argparse
import shutil
import joblib
import time
import copy

import numpy as np
import pandas as pd
import seaborn
import matplotlib.pyplot as plt
from tqdm import tqdm

from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn.metrics import confusion_matrix, roc_curve, auc
from sklearn.feature_selection import f_classif
from sklearn.inspection import permutation_importance
from imblearn.over_sampling import SMOTE
from imblearn.under_sampling import RandomUnderSampler
import shap
from xgboost import XGBClassifier
from interpret.glassbox import ExplainableBoostingClassifier
from dtreeviz import trees
import graphviz

import calibration
from exploratory_data_analysis import run_eda
import metrics
from preprocessing import TabularPreprocessor, TabularIntraFoldPreprocessor
from feature_selection import univariate_feature_selection, mrmr_feature_selection, FeatureSelector
from explainability_tools import plot_importances, plot_shap_features, plot_partial_dependences, surrogate_model


def create_path_if_not_exist(path):
    """
    Create provided path if path does not exist yet

    :param path: String indicating path to check
    :return: None
    """
    if not os.path.exists(path):
        os.makedirs(path)


def convert_str_to_container(string, container_type="tuple"):
    """
    Take string flanked with brackets and convert to container; contained elements will be auto cast;
    output will be wrapped in a list

    :param string: string which shall be converted
    :param container_type: string indicating which container to use; options are "tuple" and "list"
    :return: converted container object
    """

    if ", " not in string:
        raise ValueError(f"{string} is not a list")

    if container_type == "tuple":
        brackets = ["(", ")"]
    else:
        brackets = ["[", "]"]

    containers_to_be = string.split(brackets[1] + ", ")
    containers_to_be = [val.replace(brackets[0], "").replace(brackets[1], "").split(", ") for val in containers_to_be]

    container_objs = []
    for container_to_be in containers_to_be:
        if container_type == "tuple":
            container_objs.append(tuple([estimate_type(val) for val in container_to_be]))
        else:
            container_objs.append([estimate_type(val) for val in container_to_be])

    return container_objs


def str_to_bool(s):
    """Convert string to boolean"""

    if s == "True" or s == "true":
        return True
    if s == "False" or s == "false":
        return False
    raise ValueError("Not Boolean Value!")


def str_to_none(s):
    """Convert string to None"""

    if s == "None":
        return None
    raise ValueError("Not None Value!")


def estimate_type(var):
    """guesses the str representation of the variable"s type"""

    # Return if not string in the first place
    if not isinstance(var, str):
        return var

    # Guess string representation, defaults to string if others don't pass
    for caster in (str_to_bool, int, float, str_to_none, convert_str_to_container, str):
        try:
            return caster(var)
        except ValueError:
            pass


def auto_cast_string(string):
    """
    Automatic casting of elements within a container

    CAVE: If string to be cast contains a container such as a list, this type must be homogeneous if multiple values
    are included

    :param string: String to be cast
    :return: List containing the casted value(s)
    """

    casted = []

    if string[0] == "(" and string[-1] == ")":
        casted = convert_str_to_container(string, container_type="tuple")
    elif string[0] == "[" and string[-1] == "]":
        casted = convert_str_to_container(string, container_type="list")
    else:
        list_obj = string.split(", ")
        for value in list_obj:
            casted.append(estimate_type(value))

    return casted


def load_hyperparameters(model, config):
    """
    Obtain parameter grids (e.g. for hyperparameter optimization) from loaded configuration file

    :param model: Classifier object implementing .get_params() method such as of type sklearn.base.BaseEstimator
    :param config: configparser.ConfigParser() containing the parameters
    :return: dict containing the parameter grids
    """

    # Initialize output parameter grid
    param_grid = {}

    # Obtain all parameters available for the provided model
    params = model.get_params()

    # Iterate over each parameter
    for param in params:

        try:
            # Cast each string parameter from config file to the most reasonable type
            param_grid[param] = auto_cast_string(config[param])
        except KeyError:
            # Set parameter to default if missing in config file
            param_grid[param] = [model.get_params()[param]]

    return param_grid


def save_cumulative_confusion_matrix(cms, label_names, clf_name, save_path):
    """
    Create cumulative confusion matrix from list of matrices and save as CSV and PNG

    :param label_names: list containing names of labels
    :param clf_name: str indicating name of classifier
    :param save_path: str indicating folder path to save output files to
    """

    label_names = sorted(label_names)

    seaborn.heatmap(cms, annot=True, cmap="Blues", fmt="g")
    plt.xlabel("Predicted")
    plt.ylabel("Actual")
    plt.title("{} - Confusion matrix".format(clf_name))
    plt.savefig(os.path.join(save_path, f"confusion_matrix-{clf_name}.svg"))
    plt.close()

    # Save confusion matrix as CSV
    cm_df = pd.DataFrame(cms,
                         columns=[str(name) + " (actual)" for name in label_names],
                         index=[str(name) + " (predicted)" for name in label_names])
    cm_df.to_csv(os.path.join(save_path, f"confusion_matrix-{clf_name}.csv"), sep=";")


def save_overall_performances(overall_performances, classifier_names, save_path, decimals=4, verbose=True):
    """
    Create and save a CSV and corresponding PNG with the given performances
    :param overall_performances: pandas.DataFrame containing the performance metrics and corresponding values
    :param classifier_names: list or np.array 1D indicating the names of the employed classifiers
    :param save_path: str indicating the path to save the result files to
    :param decimals: number of decimal places to round to before saving and plotting performance metrics
    :param verbose: Boolean indicating whether to display additional output information
    """

    # Round overall performances to provided number of digits
    overall_performances = overall_performances.astype("float").round(decimals)

    # Save result table with all classifiers performances
    colors = ["dimgray", "gray", "darkgray", "silver", "lightgray", "gainsboro", "maroon"]
    overall_performances.to_csv(os.path.join(save_path, "overall_performances.csv"), sep=";")

    # Separate performances from confidence intervals
    performances = overall_performances[[col for col in overall_performances.columns if not col.endswith("_95ci")]]
    confidences = overall_performances[[col for col in overall_performances.columns if col.endswith("_95ci")]]
    confidences.columns = [col[:-5] for col in confidences.columns]

    # Set figure dimensions
    fig, ax = plt.subplots(figsize=(5, 4))

    # Create bar plot and add 95 confidence interval error bars
    performances.plot.bar(rot=45, color=colors, figsize=(4 + (len(classifier_names) - 1) * 1.5, 4),
                          yerr=confidences, capsize=5, ax=ax) \
        .legend(loc="upper right")

    if verbose is True:
        print("[Results] Displaying performance")
        print(overall_performances)

    # Adjust legend position so it doesn't mask any bars
    handles = [plt.Rectangle((0, 0), 1, 1, color=color) for color in colors]
    plt.legend(handles, [col.upper() for col in performances.columns], bbox_to_anchor=(1.05, 1), loc=2,
               borderaxespad=0.)

    # Save and display performance plot
    plt.yticks(np.arange(0, 1.1, 0.1))
    plt.ylim(0, 1.0)
    plt.title("Overall performance")
    plt.grid(True, axis="y", linestyle="-")
    plt.gca().set_axisbelow(True)
    plt.subplots_adjust(left=0.2, bottom=0.2, right=0.8, top=0.8, wspace=0.2, hspace=0.2)
    plt.tight_layout()
    plt.savefig(os.path.join(save_path, "performances_barplot.svg"))
    plt.close()


def plot_performance_boxplot(foldwise_performance, save_path):
    """
    Plot and save overall performance boxplots

    :param foldwise_performance: pd.DataFrame containing performance metrics for each classifier
    """

    colors = ["dimgray", "gray", "darkgray", "silver", "lightgray", "gainsboro", "maroon"]

    # Format data to long format
    foldwise_performance = pd.melt(foldwise_performance.drop("fold", axis="columns"),
                                   id_vars=['algorithm'], var_name='metric', value_name='value')

    for clf in np.unique(foldwise_performance.algorithm):
        df = foldwise_performance[foldwise_performance.algorithm == clf]

        # Set figure dimensions
        fig, ax = plt.subplots(figsize=(5, 3.8))

        seaborn.stripplot(x="algorithm",
                          y="value",
                          hue="metric",
                          data=df,
                          jitter=True,
                          palette=["white"],
                          edgecolor="black",
                          split=True,
                          linewidth=1,
                          alpha=0.2, ax=ax)

        seaborn.boxplot(x="algorithm",
                         y="value",
                         hue="metric",
                         data=df,
                         palette=colors,
                         fliersize=0,
                         showmeans=True,
                         meanprops={"marker": "s",
                                    "markerfacecolor": "white",
                                    "markeredgecolor": "black",
                                    "markersize": "10"},
                         ax=ax
                         )

        handles, labels = ax.get_legend_handles_labels()
        performance_metrics = [label.upper() for label in labels[0:7]]
        plt.legend(handles[0:7], performance_metrics, bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)

        plt.title(f"{clf.upper()} performance metrics")
        plt.yticks(np.arange(0, 1.1, 0.1))
        plt.xticks([])
        plt.ylim(0, 1.0)
        plt.xlabel("")
        plt.ylabel("")

        # Save plot to results
        plt.grid(True, axis="y", linestyle="-")
        plt.gca().set_axisbelow(True)
        plt.subplots_adjust(left=0.2, bottom=0.2, right=0.8, top=0.8, wspace=0.2, hspace=0.2)
        plt.tight_layout()
        plt.savefig(os.path.join(save_path, f"performances_boxplot_{clf}.svg"))
        plt.close()


def plot_roc_curve(tprs, fpr_foldwise, tpr_foldwise, clf, base_fpr, save_path):
    """
    Plotting for ROC curves in binary classifiers
    :param tprs: np.ndarray 1D True positive rates
    :param fpr_foldwise: np.ndarray 1D Fold-wise saved false positive rates
    :param tpr_foldwise: np.ndarray 1D
    :param clf: str Name of classifier
    :param base_fpr: np.ndarray 1D base false positive rate
    :param save_path: str path where plot will be saved
    """

    # Set figure dimensions
    fig, ax = plt.subplots(figsize=(5, 4))

    auc_foldwise = []
    for fpr_fold, tpr_fold in zip(fpr_foldwise[clf], tpr_foldwise[clf]):
        auc_foldwise.append(auc(fpr_fold, tpr_fold))

    auc_overall = np.round(np.sum(auc_foldwise) / len(auc_foldwise), 3)

    tprs[clf] = np.array(tprs[clf])
    mean_tprs = tprs[clf].mean(axis=0)
    std = tprs[clf].std(axis=0)

    tprs_upper = np.minimum(mean_tprs + std, 1)
    tprs_lower = mean_tprs - std

    std_overall = np.round(np.sum(std) / len(std), 3)

    plt.fill_between(base_fpr, tprs_lower, tprs_upper, facecolor="lightcoral", alpha=0.3, edgecolor="none",
                     label="mean \u00B1 1 std.dev.")

    first_entry = True
    for fpr_fold, tpr_fold in zip(fpr_foldwise[clf], tpr_foldwise[clf]):
        if first_entry:
            plt.plot(fpr_fold, tpr_fold, "maroon", alpha=0.15, linewidth="1", label="foldwise ROCs")
            first_entry=False
        else:
            plt.plot(fpr_fold, tpr_fold, "lightgray", linewidth="1")

    plt.plot([0, 1], [0, 1], "--", color="black", linewidth="1", label="random ROC")
    plt.plot(base_fpr, mean_tprs, "maroon", label=f"mean ROC (AUC {auc_overall} \u00B1 {std_overall})")

    plt.xlim([-0.01, 1.01])
    plt.ylim([-0.01, 1.01])
    plt.ylabel("True Positive Rate")
    plt.xlabel("False Positive Rate")
    plt.legend()

    plt.title(f"Receiver operating characteristic (ROC) curve for {clf.upper()}")
    plt.axis("square")
    plt.savefig(os.path.join(save_path, f"roc_curve-{clf}.svg"))
    plt.close()


def convert_special_characters(array):
    """
    Convert special characters causing issues when contained in file names to alternative characters
    :param array: np.ndarray 1D or list containing strings to be replaced
    :return: np.ndarray 1D containing the strings with replaced characters
    """

    array_converted = []

    characters_to_replace = ["/", "\\", "#", "%", "&", "$", "!", "'", "\"", ":", "@", ")", "{", "}"]
    replace_by = ["-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "(", ")"]

    for element in array:
        for i, char in enumerate(characters_to_replace):
            element = str(element).replace(char, replace_by[i])

        array_converted.append(element)

    return np.array(array_converted)


class Model(object):
    """
    Model class containing model-specific information
    """
    def __init__(self, model_name="model"):
        self.model_name = model_name
        self.estimator = None
        self.hyperparameter_grid = None


def run_pipeline(settings_path):
    """
    Run EtaML pipeline
    :param settings_path: str indicating path to settings file in INI format containing run configuration
    """

    config = configparser.ConfigParser()
    config.read(settings_path)
    
    verbose = config["Display"]["verbose"] == "True"

    input_data_path = config["Data"]["input_data_file_path"]
    input_file_separator = config["Data"]["input_data_file_separator"]
    output_path = config["Data"]["output_data_folder_path"]
    label_name = config["Data"]["label_column_name"]

    max_missing_ratio = float(config["Preprocessing"]["max_missing_ratio"])
    number_of_selected_features = config["Preprocessing"]["number_of_selected_features"]  # For each fold separately
    imputation_method = config["Preprocessing"]["imputation_method"]  # For each fold separately

    perform_reporting = config["EDA"]["perform_reporting"] == "True"
    perform_umap = config["EDA"]["perform_umap"] == "True"
    perform_tsne = config["EDA"]["perform_tsne"] == "True"
    perform_pca = config["EDA"]["perform_pca"] == "True"

    perform_calibration = config["Calibration"]["perform_calibration"] == "True"

    num_folds = int(config["Training"]["number_of_folds"])
    test_set_ratio = float(config["Training"]["test_set_ratio"])
    load_custom_folds = config["Training"]["load_custom_folds"] == "True"
    custom_folds_file_path = config["Training"]["custom_folds_file_path"]
    custom_folds_file_separator = config["Training"]["custom_folds_file_separator"]

    classifiers_to_run = config["Classifiers"]["classifiers_to_run"].split(", ")

    perform_permutation_importance = config["XAI"]["perform_permutation_importance"] == "True"
    perform_shap = config["XAI"]["perform_shap"] == "True"
    perform_surrogate_modeling = config["XAI"]["perform_surrogate_modeling"] == "True"
    perform_partial_dependence_plotting = config["XAI"]["perform_partial_dependence_plotting"] == "True"

    plot_roc_curves = config["Plotting"]["plot_roc_curves"] == "True"

    # Adapt parameters from INI file based on overruling parameters
    if load_custom_folds:
        custom_folds_table = pd.read_csv(custom_folds_file_path, sep=custom_folds_file_separator, index_col=0)
        num_folds = len(np.unique(custom_folds_table["Fold"].values))

        if verbose is True:
            print(f"[Settings] Overwriting parameter 'num_folds' based on {custom_folds_file_path}: "
                  f"new number of folds is {num_folds}")
            print(f"[Settings] Parameter 'test_set_ratio' will be ignored since 'load_custom_folds' is True")

    # Convert feature number to int if possible
    try:
        number_of_selected_features = int(number_of_selected_features)
    except ValueError:
        pass

    # Set output paths
    input_data_and_config_path = os.path.join(output_path, r"Results/Input_data/")
    eda_result_path = os.path.join(output_path, r"Results/EDA/")
    explainability_result_path = os.path.join(output_path, r"Results/XAI/")
    model_result_path = os.path.join(output_path, r"Results/Models/")
    performance_result_path = os.path.join(output_path, r"Results/Performance/")
    intermediate_data_path = os.path.join(output_path, r"Results/Intermediate_data")
    calibration_path = os.path.join(output_path, r"Results/Calibration")

    # Create save directories if they do not exist yet
    for path in [eda_result_path, explainability_result_path, model_result_path, performance_result_path,
                 intermediate_data_path, calibration_path, input_data_and_config_path]:
        create_path_if_not_exist(path)

    # Save input table and config in Input_data folder
    shutil.copyfile(input_data_path, os.path.join(input_data_and_config_path, "input_table.csv"))
    shutil.copyfile(settings_path, os.path.join(input_data_and_config_path, "settings.ini"))

    # Save custom folds if used
    if load_custom_folds:
        shutil.copyfile(custom_folds_file_path, os.path.join(input_data_and_config_path, "custom_folds.csv"))

    # Load data to table
    df = pd.read_csv(input_data_path, sep=input_file_separator, index_col=0)
    print(f"[Loading] Data successfully loaded from {input_data_path}")

    # Remove special characters from column names to avoid issues with saving file names
    df.columns = convert_special_characters(df.columns)
    label_name = convert_special_characters([label_name])[0]

    if perform_reporting is True:
        # Perform EDA and save results
        run_eda(features=df.drop(label_name, axis="columns"),
                labels=df[label_name],
                label_column=label_name,
                save_path=eda_result_path,
                analyses_to_run=["pandas_profiling"],
                verbose=verbose)

    # Perform one hot encoding of categorical features before standard scaling in EDA visualizations
    categorical_mask = df.dtypes == object
    categorical_columns = df.columns[categorical_mask].tolist()

    # Perform standardized preprocessing
    preprocessor = TabularPreprocessor(label_name=label_name,
                                       one_hot_encoder_path=os.path.join(intermediate_data_path,
                                                                         f"one_hot_encoder.joblib"),
                                       label_encoder_path=os.path.join(intermediate_data_path,
                                                                       "label_encoder.joblib"),
                                       max_missing_ratio=max_missing_ratio)
    df = preprocessor.fit_transform(df)

    # Obtain dimensionality reduction techniques to be run from config
    dimensionality_reductions_to_run = []
    if perform_umap is True:
        dimensionality_reductions_to_run.append("umap")
    if perform_tsne is True:
        dimensionality_reductions_to_run.append("tsne")
    if perform_pca is True:
        dimensionality_reductions_to_run.append("pca")

    if dimensionality_reductions_to_run:
        # Perform dimensionality reductions
        run_eda(features=df.drop(label_name, axis="columns"),
                labels=df[label_name],
                label_column=label_name,
                save_path=eda_result_path,
                analyses_to_run=dimensionality_reductions_to_run,
                verbose=verbose)

    # Separate data into training and test
    y = df[label_name]
    x = df.drop(label_name, axis="columns")

    # Get data characteristics
    feature_names = x.columns
    num_classes = len(np.unique(y))

    # # Set n_neighbors KNN parameter
    # if knn_param_grid["n_neighbors"] == ["adaptive"]:
    #     knn_param_grid["n_neighbors"] = [int(val) for val in np.round(np.sqrt(x.shape[1])) + np.arange(5) + 1] +\
    #                                     [int(val) for val in np.round(np.sqrt(x.shape[1])) - np.arange(5) if val >= 1]

    # Initialize classifiers
    initialized_classifiers = {"ebm": ExplainableBoostingClassifier(),
                               "knn": KNeighborsClassifier(),
                               "dt": DecisionTreeClassifier(),
                               "nn": MLPClassifier(),
                               "rf": RandomForestClassifier(),
                               "xgb": XGBClassifier(),
                               "svm": SVC(),
                               "lgr": LogisticRegression()}

    # Create model objects for each classifier
    clfs = {}
    for clf in classifiers_to_run:
        # Initialize model object
        clfs[clf] = Model(model_name=clf)
        clfs[clf].estimator = initialized_classifiers[clf]

        # Set hyperparameter grid
        hyperparams = config[f"{clf.upper()}_hyperparameters"]
        param_grid = load_hyperparameters(clfs[clf].estimator, hyperparams)
        clfs[clf].hyperparameter_grid = param_grid

    if verbose is True:
        print(f"[Model training] Starting model training")

    # Initialize fold-wise and classifier-wise prediction table
    foldwise_predictions = pd.DataFrame(columns=["fold", "algorithm", "ground_truth", "prediction", "probability"])

    # Initialize fold-wise and classifier-wise performance table
    foldwise_performance = pd.DataFrame()

    # Initialize fold-wise and classifier-wise importance container
    classifierwise_foldwise_importance = pd.DataFrame()

    # Initialize performance containers for ROC curve
    if num_classes == 2 and plot_roc_curves:
        base_fpr = np.linspace(0, 1, 101)
        tprs = {clf: [] for clf in clfs}
        fpr_foldwise = {clf: [] for clf in clfs}
        tpr_foldwise = {clf: [] for clf in clfs}

    # Iterate over folds
    tqdm_bar = tqdm(np.arange(num_folds))
    for fold_index in tqdm_bar:

        if load_custom_folds is True:

            # Load current custom fold
            current_fold = np.sort(np.unique(custom_folds_table.Fold))[fold_index]
            current_samples = custom_folds_table.loc[custom_folds_table.Fold == current_fold]

            # Remove samples from custom folds if they were previously removed
            for sample in current_samples.index:
                if sample not in y.index:
                    current_samples.drop(sample, axis="rows", inplace=True)

                    if verbose is True:
                        print(f"\n[Warning] Sample '{sample}' was removed in a previous step but was included in the"
                              f"list of custom folds. Sample will be excluded from analysis!")

            # Load custom train and test fold samples
            current_train_samples = current_samples.loc[current_samples.Set == "train"]
            current_test_samples = current_samples.loc[current_samples.Set == "test"]

            x_train = x.loc[current_train_samples.index]
            x_test = x.loc[current_test_samples.index]
            y_train = y.loc[current_train_samples.index]
            y_test = y.loc[current_test_samples.index]

            idx_train = x_train.index
            idx_test = x_test.index

        else:
            # Split into training and test data
            x_train, x_test, y_train, y_test, idx_train, idx_test = train_test_split(x, y,
                                                                                     df.index,  # Stratify indices
                                                                                     test_size=test_set_ratio,
                                                                                     stratify=y,
                                                                                     shuffle=True,
                                                                                     random_state=fold_index)

        # Check whether each label exists in each fold
        omit_fold = False
        for unique_label in np.unique(y):
            if unique_label not in y_train.values or unique_label not in y_test.values:
                unique_label_original = preprocessor.label_encoder.inverse_transform([unique_label])[0]
                print(f"[Warning] Label '{unique_label_original}' was not found in both train and test set of fold "
                      f"with index {fold_index}. This is likely to cause problems in the downstream process. Omitting "
                      f"Fold!")
                omit_fold = True

        if omit_fold is True:
            continue

        # Perform standardization and feature imputation
        intra_fold_preprocessor = TabularIntraFoldPreprocessor(imputation_method=imputation_method,
                                                               k="automated",
                                                               normalization="standardize",
                                                               random_state=int(fold_index))
        intra_fold_preprocessor = intra_fold_preprocessor.fit(x_train)
        x_train = intra_fold_preprocessor.transform(x_train)
        x_test = intra_fold_preprocessor.transform(x_test)

        # Perform feature selection
        selected_indices, x_train, x_test = mrmr_feature_selection(x_train.values,
                                                                   y_train.values,
                                                                   x_test.values,
                                                                   # score_func=f_classif,
                                                                   num_features=number_of_selected_features)
        feature_names_selected = feature_names[selected_indices]

        # SMOTE
        if num_classes == 2:
            smote = SMOTE(random_state=fold_index, sampling_strategy=1)
        else:
            smote = SMOTE(random_state=fold_index, sampling_strategy="not majority")
        x_train, y_train = smote.fit_resample(x_train, y_train)

        # Iterate over classifiers
        for clf_index, clf in enumerate(clfs):

            # Hyperparameter tuning and keep model trained with the best set of hyperparameters
            optimized_model = RandomizedSearchCV(clfs[clf].estimator,
                                                 param_distributions=clfs[clf].hyperparameter_grid,
                                                 cv=auto_cast_string(config["Training"]["randomizedsearchcv_cv"])[0],
                                                 n_iter=
                                                 auto_cast_string(config["Training"]["randomizedsearchcv_n_iter"])[0],
                                                 scoring="roc_auc",
                                                 random_state=fold_index)

            # Train tuned model
            optimized_model.fit(x_train, y_train)

            if perform_calibration is True:

                # Create backup of uncalibrated model
                uncalibrated_model = copy.deepcopy(optimized_model)

                # Perform probability calibration of fold model using ensemble approach
                optimized_model = calibration.calibrate(model=optimized_model,
                                                        features=x_train,
                                                        labels=y_train,
                                                        clf_name=clf,
                                                        verbose=False)

            # Compute TPRs and FPRs for ROC curves
            if num_classes == 2 and plot_roc_curves:
                y_proba = optimized_model.predict_proba(x_test)
                fpr, tpr, _ = roc_curve(y_test, y_proba[:, 1])

                tpr_foldwise[clf].append(tpr)
                fpr_foldwise[clf].append(fpr)
                tpr = np.interp(base_fpr, fpr, tpr)
                tpr[0] = 0.0
                tprs[clf].append(tpr)

            # Compute permutation feature importance scores on training and validation data
            importances_train = permutation_importance(optimized_model, x_train, y_train,
                                                           n_repeats=30,
                                                           scoring="roc_auc_ovr",
                                                           n_jobs=10,  # TODO: adjust and automate
                                                           random_state=fold_index)
            importances_val = permutation_importance(optimized_model, x_test, y_test,
                                                         n_repeats=30,
                                                         scoring="roc_auc_ovr",
                                                         n_jobs=10,  # TODO: adjust and automate
                                                         random_state=fold_index)

            # Add importance mean and std dev to overall container
            if perform_permutation_importance:
                for index, feat in enumerate(feature_names_selected):    # Add importance score for selected features
                    classifierwise_foldwise_importance = classifierwise_foldwise_importance.append(
                        {"clf": clf,
                         "fold": fold_index,
                         "feature": feat,
                         "metric": "mean_train",
                         "value": importances_train.importances_mean[index]},
                        ignore_index=True)
                    classifierwise_foldwise_importance = classifierwise_foldwise_importance.append(
                        {"clf": clf,
                         "fold": fold_index,
                         "feature": feat,
                         "metric": "std_train",
                         "value": importances_train.importances_std[index]},
                        ignore_index=True)
                    classifierwise_foldwise_importance = classifierwise_foldwise_importance.append(
                        {"clf": clf,
                         "fold": fold_index,
                         "feature": feat,
                         "metric": "mean_val",
                         "value": importances_val.importances_mean[index]},
                        ignore_index=True)
                    classifierwise_foldwise_importance = classifierwise_foldwise_importance.append(
                        {"clf": clf,
                         "fold": fold_index,
                         "feature": feat,
                         "metric": "std_val",
                         "value": importances_val.importances_std[index]},
                        ignore_index=True)

            # Get fold-wise predictions
            y_pred = optimized_model.predict(x_test)

            # Get fold-wise probability predictions
            y_prob = optimized_model.predict_proba(x_test)

            if num_classes == 2:
                # For binary classification, only use probability for higher class
                y_prob = y_prob[:, 1]
            else:
                # For multiclass classification, use a list of lists, each containing the probability per class
                y_prob = [multiclass_probs for multiclass_probs in y_prob]

            # Create fold specific prediction table
            fold_predictions = pd.DataFrame(index=idx_test)
            fold_predictions.index.name = "Sample ID"
            fold_predictions["fold"] = [fold_index, ] * len(y_test)
            fold_predictions["algorithm"] = [clf, ] * len(y_test)
            fold_predictions["ground_truth"] = y_test
            fold_predictions["prediction"] = y_pred
            fold_predictions["probability"] = y_prob

            # Store fold-wise predictions
            foldwise_predictions = pd.concat([foldwise_predictions, fold_predictions])

            # Save foldwise predictions to result folder
            retry = True
            while retry is True:
                try:
                    foldwise_predictions.to_csv(os.path.join(performance_result_path, "foldwise_predictions.csv"), sep=";")
                    retry = False
                except PermissionError:
                    print("[Warning] File 'foldwise_predictions.csv' is open. Close file to continue Reattempting in 10 seconds.")
                    time.sleep(10)

            # Compute performance for current fold
            fold_performance = {}
            
            fold_performance["fold"] = fold_index
            fold_performance["algorithm"] = clf
            fold_performance["acc"] = metrics.accuracy(y_test, y_pred)
            fold_performance["sns"] = metrics.sensitivity(y_test, y_pred)
            fold_performance["spc"] = metrics.specificity(y_test, y_pred)
            fold_performance["ppv"] = metrics.positive_predictive_value(y_test, y_pred)
            fold_performance["npv"] = metrics.negative_predictive_value(y_test, y_pred)
            fold_performance["bacc"] = metrics.balanced_accuracy(y_test, y_pred)
            fold_performance["auc"] = metrics.roc_auc(y_test, y_prob)

            foldwise_performance = foldwise_performance.append(fold_performance, ignore_index=True)

            # Save foldwise performance to result folder
            retry = True
            while retry is True:
                try:
                    foldwise_performance.to_csv(os.path.join(performance_result_path, "foldwise_performance.csv"),
                                                sep=";", index=False)
                    retry = False
                except PermissionError:
                    print("[Warning] File 'foldwise_performance.csv' is open. Close file to continue Reattempting in 10 seconds.")
                    time.sleep(10)

            # Progressbar
            last_auc = np.round(fold_performance["auc"], 3)
            if verbose is True:
                tqdm_bar.set_description(str(f"[Model training] Finished folds (last {clf} AUC: {last_auc})"))

    # Save foldwise permutation importances to results
    classifierwise_foldwise_importance.to_csv("classifierwise_foldwise_importance.csv", sep=";")

    # Initialize overall performance table including 95 % confidence intervals
    overall_performances = pd.DataFrame(columns=["acc", "sns", "spc", "ppv", "npv", "bacc", "auc",
                                                 "acc_95ci", "sns_95ci", "spc_95ci", "ppv_95ci",
                                                 "npv_95ci", "bacc_95ci", "auc_95ci"],
                                        index=list(clfs.keys()))

    # Create overall performance box plots
    plot_performance_boxplot(foldwise_performance, save_path=performance_result_path)

    # Average foldwise performance metrics and calculate confidence intervals
    for clf in np.unique(foldwise_performance.algorithm):
        for metric in foldwise_performance.columns:
            if metric == "algorithm" or metric == "cm" or metric == "fold":
                continue

            # Add performance metric to overall performance container
            metric_sum = np.sum(foldwise_performance[foldwise_performance["algorithm"] == clf][metric])
            overall_performances.at[clf, metric] = metric_sum / num_folds

            # Add confidence intervals for performance metrics to overall performance container
            metric_stddev = np.std(foldwise_performance[foldwise_performance["algorithm"] == clf][metric])
            overall_performances.at[clf, metric + "_95ci"] = (1.96 * metric_stddev / np.sqrt(num_folds))

        # Get confusion matrix over all folds
        cm = confusion_matrix(list(foldwise_predictions[foldwise_predictions.algorithm == clf].ground_truth.values),
                              list(foldwise_predictions[foldwise_predictions.algorithm == clf].prediction.values))

        # Save cumulative confusion matrix as CSV and PNG
        save_cumulative_confusion_matrix(cm,
                                         label_names=np.sort(np.unique(y)),
                                         clf_name=clf,
                                         save_path=performance_result_path)

        # ROC curve
        if num_classes == 2 and plot_roc_curves:
            plot_roc_curve(tprs=tprs,
                           fpr_foldwise=fpr_foldwise,
                           tpr_foldwise=tpr_foldwise,
                           base_fpr=base_fpr,
                           clf=clf,
                           save_path=performance_result_path)

    # Save overall performance metrics to PNG bar plot and CSV
    save_overall_performances(overall_performances.round(decimals=4),
                              classifier_names=classifiers_to_run,
                              save_path=performance_result_path,
                              verbose=True)

    # Preprocess data for creation of final model
    intra_fold_preprocessor = TabularIntraFoldPreprocessor(imputation_method=imputation_method,
                                                           k="automated",
                                                           normalization="standardize",
                                                           imputer_path=os.path.join(intermediate_data_path,
                                                                                     f"imputer.joblib"),
                                                           scaler_path=os.path.join(intermediate_data_path,
                                                                                    f"scaler.joblib"),
                                                           random_state=0)

    x_preprocessed = intra_fold_preprocessor.fit_transform(x)

    # Save preprocessed data
    x_preprocessed_df = pd.DataFrame(data=x_preprocessed,
                                     index=x.index,
                                     columns=feature_names)
    x_preprocessed_df.to_csv(os.path.join(intermediate_data_path, "preprocessed_features.csv"),
                             sep=";")

    y_df = pd.DataFrame(data=y, columns=[label_name])
    y_df.to_csv(os.path.join(intermediate_data_path, "preprocessed_labels.csv"), sep=";")

    # Feature selection for final model
    selected_indices_preprocessed, x_preprocessed, _ = mrmr_feature_selection(x_preprocessed,
                                                                              y,
                                                                              # score_func=f_classif,
                                                                              num_features=number_of_selected_features)

    # Get feature names selected
    feature_names_selected = feature_names[selected_indices_preprocessed]

    # Save selected feature names
    feature_selector = FeatureSelector()
    feature_selector = feature_selector.fit(feature_names_selected)
    joblib.dump(feature_selector, os.path.join(intermediate_data_path, "feature_selector.joblib"))

    # Perform oversampling (after feature selection as recommended in the original publication)
    if num_classes == 2:
        smote = SMOTE(random_state=0, sampling_strategy=1)
    else:
        smote = SMOTE(random_state=0, sampling_strategy="not majority")
    x_preprocessed_smoted, y = smote.fit_resample(x_preprocessed, y)

    # Iterate over classifiers, create final models and apply XAI techniques
    for clf in clfs:

        # Setup final model
        model = clfs[clf].estimator

        # Add feature names enabling interpretability of output plots (only needed for some algorithms like ebm)
        if clf == "ebm":
            model.set_params(**{"feature_names": feature_names_selected})

        # Hyperparameter tuning for final model
        optimized_model = RandomizedSearchCV(model,
                                             param_distributions=clfs[clf].hyperparameter_grid,
                                             cv=auto_cast_string(config["Training"]["randomizedsearchcv_cv"])[0],
                                             n_iter=auto_cast_string(config["Training"]["randomizedsearchcv_n_iter"])[
                                                 0],
                                             scoring="roc_auc",
                                             random_state=0)

        optimized_model.fit(x_preprocessed_smoted, y)
        best_params = optimized_model.best_params_
        optimized_model = optimized_model.best_estimator_

        # Save final model to file without calibration
        with open(os.path.join(model_result_path, f"uncalibrated_{clf}_model.joblib"), "wb") as file:
            joblib.dump(optimized_model, file)

        if perform_calibration is True:

            # Create backup of uncalibrated model
            uncalibrated_model = copy.deepcopy(optimized_model)

            # Perform probability calibration of final model using ensemble approach
            optimized_model = calibration.calibrate(model=optimized_model,
                                                    features=x_preprocessed_smoted,
                                                    labels=y,
                                                    clf_name=clf,
                                                    verbose=verbose)

            # Create and save calibration curve of final model
            if num_classes == 2:
                calibration.create_calibration_curve(original_model=uncalibrated_model,
                                                     calibrated_model=optimized_model,
                                                     features=x_preprocessed_smoted,
                                                     labels=y,
                                                     calibration_path=calibration_path,
                                                     clf_name=clf,
                                                     show=False)

            # Save final model to file after calibration
            with open(os.path.join(model_result_path, f"calibrated_{clf}_model.joblib"), "wb") as file:
                joblib.dump(optimized_model, file)

        # Save hyperparameters of final model to JSON file
        with open(os.path.join(model_result_path, f"{clf}_optimized_hyperparameters.json"), "w") as file:

            param_dict_json_conform = {}  # Necessary since JSON doesn't take some data types such as int32
            for key in best_params:
                try:
                    param_dict_json_conform[key] = float(best_params[key])
                except ValueError:
                    param_dict_json_conform[key] = best_params[key]
                except TypeError:
                    param_dict_json_conform[key] = best_params[key]

            json.dump(param_dict_json_conform, file, indent=4)

        if perform_permutation_importance:

            # Get mean of feature importance scores and standard deviation over all folds
            foldaveraged_importances = classifierwise_foldwise_importance[classifierwise_foldwise_importance["clf"] == clf].groupby(["feature", "metric"]).mean()

            # Get features which are in final model and all features with non-zero importances during training
            relevant_training_features = foldaveraged_importances.index.get_level_values(0).values

            importance_features = list(set(list(feature_names_selected) + list(relevant_training_features)))

            overall_importances = {}
            for feat_name in importance_features:
                for metric in ["mean_train", "std_train", "mean_val", "std_val"]:
                    if metric not in overall_importances.keys():
                        overall_importances[metric] = []

                    if foldaveraged_importances.query(f"feature == '{feat_name}' and metric == '{metric}'").empty:
                        overall_importances[metric].append(0)
                    else:
                        overall_importances[metric].append(foldaveraged_importances.query(f"feature == '{feat_name}' and metric == '{metric}'").value[0])

            # Plot feature importances as determined using training and validation data
            plot_title_permutation_importance = f"permutation_importance_{clf}"

            importances_save_path = os.path.join(explainability_result_path,
                                                 "Permutation_importances")
            create_path_if_not_exist(importances_save_path)

            train_importances_save_path = os.path.join(importances_save_path,
                                                       plot_title_permutation_importance + "-train.svg")
            plot_importances(importances_mean=overall_importances["mean_train"],
                             importances_std=overall_importances["std_train"],
                             feature_names=importance_features,
                             plot_title=plot_title_permutation_importance + "-training_data",
                             order_alphanumeric=True,
                             include_top=0,
                             display_plots=False,
                             save_path=train_importances_save_path)

            test_importances_save_path = os.path.join(importances_save_path,
                                                      plot_title_permutation_importance + "-test.svg")
            plot_importances(importances_mean=overall_importances["mean_val"],
                             importances_std=overall_importances["std_val"],
                             feature_names=importance_features,
                             plot_title=plot_title_permutation_importance + "-validation_data",
                             order_alphanumeric=True,
                             include_top=0,
                             display_plots=False,
                             save_path=test_importances_save_path)

        if clf == "ebm":    # TODO: Add settings.ini parameter to decide whether ebm interpretability shall be performed
            # EBM explainability
            ebm_xai_save_path = os.path.join(explainability_result_path, "Partial_dependence_plots")
            create_path_if_not_exist(ebm_xai_save_path)

            # Add interaction features to feature name list for later plotting
            feat_names_with_interactions = feature_names_selected
            for _, value in enumerate(optimized_model.feature_groups_):
                if len(value) == 2:     # Add interaction features to feature names
                    interaction_feat_name = f"{feature_names_selected[value[0]]} x {feature_names_selected[value[1]]}"
                    feat_names_with_interactions = feat_names_with_interactions.append(pd.Index([interaction_feat_name]))

            optimized_model.set_params(**{"feature_names": feat_names_with_interactions})
            ebm_global = optimized_model.explain_global()

            # Create plots
            for index, value in enumerate(optimized_model.feature_groups_):
                plotly_fig = ebm_global.visualize(index)
                current_feat_name = feat_names_with_interactions[index]
                plotly_fig.write_html(os.path.join(ebm_xai_save_path, f"ebm_partial_dependence_{current_feat_name}.html"))

        if perform_partial_dependence_plotting:
            # Partial dependence plots (DPD)
            pdp_save_path = os.path.join(explainability_result_path, "Partial_dependence_plots")
            create_path_if_not_exist(pdp_save_path)
            plot_partial_dependences(model=optimized_model,
                                     x=x_preprocessed,
                                     y=y,
                                     feature_names=feature_names_selected,
                                     clf_name=clf,
                                     save_path=pdp_save_path)

        if perform_surrogate_modeling:
            # Create surrogate models
            if clf not in ["dt", "ebm"]:
                surrogate_models_save_path = os.path.join(explainability_result_path, "Surrogate_models")
                create_path_if_not_exist(surrogate_models_save_path)

                # Decision tree surrogate model
                dt_surrogate_models_save_path = os.path.join(surrogate_models_save_path,
                                                             f"dt_surrogate_model_for-{clf}.joblib")

                # Use dummy classifier to load parameter grid
                dt_surrogate_params = load_hyperparameters(DecisionTreeClassifier(),
                                                           config["Surrogate_DT_hyperparameters"])
                dt_surrogate_params = {k: dt_surrogate_params[k][0] for k in dt_surrogate_params}

                dt_surrogate_model, _ = surrogate_model(opaque_model=optimized_model,
                                                        features=x_preprocessed,
                                                        params=dt_surrogate_params,
                                                        surrogate_type="dt",
                                                        save_path=dt_surrogate_models_save_path,
                                                        verbose=True)

                # EBM surrogate model
                ebm_surrogate_models_save_path = os.path.join(surrogate_models_save_path,
                                                              f"ebm_surrogate_model_for-{clf}.joblib")

                # Use dummy classifier to load parameter grid and remove list wrapping
                ebm_surrogate_params = load_hyperparameters(ExplainableBoostingClassifier(),
                                                            config["Surrogate_EBM_hyperparameters"])
                ebm_surrogate_params = {k: ebm_surrogate_params[k][0] for k in ebm_surrogate_params}

                ebm_surrogate_model, _ = surrogate_model(opaque_model=optimized_model,
                                                         features=x_preprocessed,
                                                         params=ebm_surrogate_params,
                                                         surrogate_type="ebm",
                                                         save_path=ebm_surrogate_models_save_path,
                                                         verbose=True)

                # Create and save surrogate tree visualization
                dt_surrogate_model_visualization_save_path = os.path.join(surrogate_models_save_path,
                                                                          f"dt_surrogate_model_for-{clf}.svg")
                int_label_names = \
                    [label for label in dt_surrogate_model.classes_]
                if preprocessor.label_encoder is not None:
                    decoded_class_names = list(preprocessor.label_encoder.inverse_transform(int_label_names))
                else:
                    decoded_class_names = int_label_names

                viz = trees.dtreeviz(dt_surrogate_model, x_preprocessed, y,
                               target_name="Label",
                               feature_names=feature_names_selected,
                               class_names=decoded_class_names)
                try:
                    viz.save(dt_surrogate_model_visualization_save_path)
                except graphviz.backend.execute.ExecutableNotFound as e:
                    print(f"[Warning] Graphviz might not be correctly installed on your system. Cannot visualize "
                          f"surrogate models: {e}")

        if perform_shap:
            # SHAP analysis and plotting
            shap_save_path = os.path.join(explainability_result_path, "SHAP")
            create_path_if_not_exist(shap_save_path)
            if preprocessor.label_encoder is not None:
                decoded_class_names = list(preprocessor.label_encoder.inverse_transform(optimized_model.classes_))
            else:
                decoded_class_names = optimized_model.classes_

            plot_shap_features(model=optimized_model,
                               x=x_preprocessed,
                               index_names=x_preprocessed_df.index,
                               feature_names=feature_names_selected,
                               clf_name=clf,
                               classes=decoded_class_names,
                               save_path=shap_save_path,
                               verbose=True)


def main():
    """
    Main function obtaining command line parameters to forward to AutoML pipeline
    """

    # Get arugments from command line
    parser = argparse.ArgumentParser(description="EtaML, Explainable Tabular AutoML Platform")
    parser.add_argument("-c", "--config", help="Path to INI file containing the run configuration", required=True)
    args = vars(parser.parse_args())

    # Run pipeline using the provided config file path
    run_pipeline(args["config"])


if __name__ == "__main__":
    main()
