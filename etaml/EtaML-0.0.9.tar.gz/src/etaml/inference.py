#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Created on Oct 04 14:14 2022

Prediction of instances using a previously trained model

@author: cspielvogel
"""

import joblib
import os
import pandas as pd
import numpy as np


def main():
    project_path = "/home/cspielvogel/Tools/Supervised_ML/TabularClassificationTemplate/DPD-AI_4feats_02dec2022"
    data_path = "/home/cspielvogel/Tools/Supervised_ML/TabularClassificationTemplate/DPD-AI_4feats_14nov2022/Results/Input_data/input_table.csv"
    separator = ","

    # Load data
    data = pd.read_csv(data_path, sep=separator, index_col=0)

    # Setup pipeline
    pipeline_paths = [
        os.path.join(project_path, "Results/Intermediate_data/one_hot_encoder.joblib"),
        os.path.join(project_path, "Results/Intermediate_data/imputer.joblib"),
        os.path.join(project_path, "Results/Intermediate_data/scaler.joblib"),
        os.path.join(project_path, "Results/Intermediate_data/feature_selector.joblib"),
        os.path.join(project_path, "Results/Models/calibrated_rf_model.joblib"),
        os.path.join(project_path, "Results/Intermediate_data/label_encoder.joblib")
    ]

    # Apply transformations
    for path in pipeline_paths:

        if not os.path.isfile(path):
            print("File not found:", path)
            continue

        component = joblib.load(path)
        component_class = component.__class__.__name__

        if component_class == "KNNImputer":
            transformed = component.transform(data)
            data = pd.DataFrame(transformed, columns=data.columns)
        elif component_class == "StandardScaler":
            transformed = component.transform(data)
            data = pd.DataFrame(transformed, columns=data.columns)
        elif component_class == "FeatureSelector":
            data = component.transform(data)
        elif hasattr(component, "predict"):
            data = component.predict(data)
        elif hasattr(component, "transform"):
            transformed = component.transform(data)
            data = pd.DataFrame(transformed, columns=data.columns)
        else:
            print(f"[ERROR] Unknown object type at {path}: {component_class}")

    print("Predicted labels:\n", data)
    print(np.unique(data, return_counts=True))

    return data


if __name__ == "__main__":
    main()
