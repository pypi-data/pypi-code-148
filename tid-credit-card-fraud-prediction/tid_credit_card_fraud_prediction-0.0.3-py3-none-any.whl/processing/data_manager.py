import os
import typing as t

import joblib
import pandas as pd
from imblearn.pipeline import Pipeline

from fraud_analysis import __version__ as _version
from fraud_analysis.config.core import (
    OUTPUTS_DIR,
    PIPELINE_DEBUG_DIR,
    RAW_DATA_DIR,
    TEST_DATA_DIR,
    TRAINED_MODEL_DIR,
    config,
)


# This function load the raw dataset
def load_dataset(file_path) -> pd.DataFrame:
    """
    load_dataset: this function loads the raw data
    Args:
        file_path: path to data file
    Returns:
        dataframe(pd.DataFrame): raw data frame
    """

    if file_path.is_file():
        return pd.read_csv(
            file_path,
        )
    raise Exception(f"Raw data not found at {file_path}!")


def save_pipeline(*, pipeline_to_persist: object) -> object:
    """Persist the pipeline.x
    Saves the versioned model, and overwrites any previous
    saved models. This ensures that when the package is
    published, there is only one trained model that can be
    called, and we know exactly how it was built.
    """

    # Prepare versioned save file name
    save_file_name = f"{config.app_config.saved_pipeline_filename}{_version}.pkl"
    save_path = TRAINED_MODEL_DIR / save_file_name

    # remove all files in TRAINED_MODEL_DIR and replace any existing .pkl with
    # same name as current version of the pipeline so that we have only a single model
    # in our package.
    remove_old_pipelines(files_to_keep=[save_file_name])
    # persist model
    joblib.dump(pipeline_to_persist, save_path)

    return None


def remove_old_pipelines(*, files_to_keep: t.List[str]) -> None:
    """
    Remove old model pipelines.
    This is to ensure there is a simple one-to-one
    mapping between the package version and the model
    version to be imported and used by other applications.
    """
    do_not_delete = files_to_keep + ["__init__.py"]

    for model_file in TRAINED_MODEL_DIR.iterdir():
        if model_file.name not in do_not_delete:
            # remove file
            model_file.unlink()


def load_pipeline(*, file_name: str) -> Pipeline:
    """Load a persisted pipeline."""

    file_path = TRAINED_MODEL_DIR / file_name

    if file_path.is_file():
        trained_model = joblib.load(filename=file_path)
        return trained_model
    else:
        raise Exception(f"Pipeline version {_version} not found!")


def create_dirs():
    """
    This function check if a directory exist, if not it will create it.
    We need this function because some directories will not exist in
    the project directory (e.g., directories that contains .csv, which
    we include in .gitignore)

    Args:
        None

    Returns:
        None
    """
    l_dir_to_check = [
        RAW_DATA_DIR,
        TEST_DATA_DIR,
        TRAINED_MODEL_DIR,
        OUTPUTS_DIR,
        PIPELINE_DEBUG_DIR,
    ]

    for d in l_dir_to_check:
        CHECK_FOLDER = os.path.isdir(d)

        # If folder doesn't exist, then create it.
        if not CHECK_FOLDER:
            os.makedirs(d)
            print(f"created folder: {d}")
