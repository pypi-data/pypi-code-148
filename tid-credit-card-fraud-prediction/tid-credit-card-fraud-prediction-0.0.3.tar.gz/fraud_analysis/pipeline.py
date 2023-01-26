from feature_engine.selection import DropConstantFeatures
from feature_engine.wrappers import SklearnTransformerWrapper
from imblearn.over_sampling import SMOTE
from imblearn.pipeline import Pipeline as imb_pipeline
from imblearn.under_sampling import RandomUnderSampler
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler

from fraud_analysis.config.core import config
from fraud_analysis.processing import features as pp

# Create pipeline
data_pipeline = imb_pipeline(
    [
        # === drop qusai-constant variables === #
        # drop variables with any level that appears in X of observations
        ("drop_nzv", DropConstantFeatures(tol=config.model_config.DROP_NZV_TOL)),
        # === save feature names (of the df from the drop_nzv step) ===
        ("save_feature_names", pp.save_col_names()),
        # === standardization === #
        (
            "feature_scaling",
            SklearnTransformerWrapper(
                transformer=StandardScaler(), variables=config.model_config.VARS_TO_STD
            ),
        ),
        # === oversampling === #
        # upsample the minority classes to have 0.1 of the majority class
        (
            "oversampling",
            SMOTE(
                sampling_strategy=config.model_config.OVERSAMPLING_STRATEGY,
                random_state=config.model_config.RANDOM_STATE,
            ),
        ),
        # === undersampling ==== #
        # undersample the majority class to have 2x of minority class
        (
            "undersampling",
            RandomUnderSampler(
                sampling_strategy=config.model_config.UNDERSAMPLING_STRATEGY,
                random_state=config.model_config.RANDOM_STATE,
            ),
        ),
        # === model === #
        (
            "clf",
            RandomForestClassifier(
                random_state=config.model_config.RANDOM_STATE,
                n_estimators=config.model_config.CLF__N_ESTIMATORS,
                max_features=config.model_config.CLF__MAX_FEATURES,
                min_samples_split=config.model_config.CLF__MIN_SAMPLES_SPLIT,
            ),
        ),
    ]
)


# Create the debug pipeline by inserting the debug step
# after every step in data_pipeline

data_pipeline_debug = imb_pipeline(
    [
        # === drop qusai-constant variables === #
        # drop variables with any level that appears in X of observations
        ("drop_nzv", DropConstantFeatures(tol=config.model_config.DROP_NZV_TOL)),
        # === save feature names (of the df from the drop_nzv step) ===
        ("save_feature_names", pp.save_col_names()),
        # Debug nzv
        (
            "debug_drop_nzv",
            pp.Debug(
                step_name="drop_nzv",
            ),
        ),
        # === standardization === #
        (
            "feature_scaling",
            SklearnTransformerWrapper(
                transformer=StandardScaler(), variables=config.model_config.VARS_TO_STD
            ),
        ),
        # Debug feature_scaling
        (
            "debug_feature_scaling",
            pp.Debug(
                step_name="feature_scaling",
            ),
        ),
        # === oversampling === #
        # upsample the minority classes to have 0.1 of the majority class
        (
            "oversampling",
            SMOTE(
                sampling_strategy=config.model_config.OVERSAMPLING_STRATEGY,
                random_state=config.model_config.RANDOM_STATE,
            ),
        ),
        # Debug oversampling
        (
            "debug_oversampling",
            pp.Debug(
                step_name="oversampling",
            ),
        ),
        # === undersampling ==== #
        # undersample the majority class to have 2x of minority class
        (
            "undersampling",
            RandomUnderSampler(
                sampling_strategy=config.model_config.UNDERSAMPLING_STRATEGY,
                random_state=config.model_config.RANDOM_STATE,
            ),
        ),
        # Debug undersampling
        (
            "debug_undersampling",
            pp.Debug(
                step_name="undersampling",
            ),
        ),
        # === model === #
        (
            "clf",
            RandomForestClassifier(
                random_state=config.model_config.RANDOM_STATE,
                n_estimators=config.model_config.CLF__N_ESTIMATORS,
                max_features=config.model_config.CLF__MAX_FEATURES,
                min_samples_split=config.model_config.CLF__MIN_SAMPLES_SPLIT,
            ),
        ),
    ]
)
