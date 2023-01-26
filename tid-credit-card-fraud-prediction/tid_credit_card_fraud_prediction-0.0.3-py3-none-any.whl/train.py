"""
This module takes raw data, process it, split data
into train and validation sets, and peform imputation,up- and down-sampling,
feature selection, scaling, and modeling
with a tuned data pipeline (parameters are given in config.yml).
"""

from pathlib import Path

import pandas as pd
from sklearn.model_selection import train_test_split

import fraud_analysis.evaluate as eval
import fraud_analysis.predict as predict
from fraud_analysis.config.core import OUTPUTS_DIR, RAW_DATA_DIR, TEST_DATA_DIR, config
from fraud_analysis.pipeline import data_pipeline, data_pipeline_debug
from fraud_analysis.processing.data_manager import create_dirs, load_dataset, save_pipeline


def run_training():

    # create directories
    create_dirs()

    # import raw data
    raw = load_dataset(file_path=Path(RAW_DATA_DIR, config.app_config.raw_data_file))
    # Get selected features
    df = raw.loc[
        :, config.model_config.SELECTED_FEATURES + [config.model_config.DV]
    ].copy()

    # train test split
    X_train, X_test, y_train, y_test = train_test_split(
        df.drop(config.model_config.DV, axis="columns"),
        df.Class,
        test_size=config.model_config.TEST_SIZE,
        random_state=config.model_config.RANDOM_STATE,
        stratify=df[config.model_config.DV],
    )

    # Save X_train and y_test
    X_test.to_csv(Path(TEST_DATA_DIR, "X_test.csv"), index=False)
    y_test.to_csv(Path(TEST_DATA_DIR, "y_test.csv"), index=False)

    # Train and Evaluate the Data pipeline -----
    if config.app_config.DEBUG_PIPELINE:
        pipeline = data_pipeline_debug
    else:
        pipeline = data_pipeline

    # Estimate the test score with CV, and plot the confusion matrix and PRC
    eval.evaluate(pipeline=pipeline, X_train=X_train, y_train=y_train)

    # Fit pipeline with the entire train set
    pipeline.fit(X_train, y_train)

    # Persist the trained pipeline (when not in DEBUG_PIPELINE mode)
    if not config.app_config.DEBUG_PIPELINE:
        save_pipeline(pipeline_to_persist=data_pipeline)

    # Feature importance of trained Random Forest model
    eval.plot_feature_importance(
        data_pipeline=pipeline,
        X_train=X_train,
        out_path=Path(OUTPUTS_DIR, "feature_importance.png"),
    )

    # Make predictions on X_test using the trained pipeline ----

    # Read X_test and y_test
    X_test = load_dataset(file_path=Path(TEST_DATA_DIR, "X_test.csv"))
    y_test = load_dataset(file_path=Path(TEST_DATA_DIR, "y_test.csv"))

    # Make predictions
    res = predict.make_prediction(input_data=X_test)
    # Output final predictions
    df_final_predictions = pd.DataFrame(
        res["predictions"], columns=["predicted_is_fraud"]
    )
    df_final_predictions.to_csv(
        Path(OUTPUTS_DIR, "final_test_set_predictions.csv"), index=False
    )
    # Evaluate the model on the test set
    eval.evaluate_on_test_set(
        y_test=y_test,
        y_pred=res["predictions"],
        y_pred_scores=res["predicted_proba"],
    )


if __name__ == "__main__":
    run_training()
