import pandas as pd

from fraud_analysis import __version__ as _version
from fraud_analysis.config.core import config
from fraud_analysis.processing.data_manager import load_pipeline


def make_prediction(*, input_data: pd.DataFrame) -> dict:

    # load saved trained pipeline
    pipeline_file_name = f"{config.app_config.saved_pipeline_filename}{_version}.pkl"
    _fraud_data_pipe = load_pipeline(file_name=pipeline_file_name)

    # Get selected features
    input_data = input_data.loc[:, config.model_config.SELECTED_FEATURES].copy()
    # Make predictions using the trained pipeline
    predictions = _fraud_data_pipe.predict(X=input_data)
    predicted_proba = _fraud_data_pipe.predict_proba(X=input_data)

    results = {
        # class predictions
        "predictions": predictions,  # type: ignore
        "predicted_proba": predicted_proba,
        "version": _version,
    }

    return results
