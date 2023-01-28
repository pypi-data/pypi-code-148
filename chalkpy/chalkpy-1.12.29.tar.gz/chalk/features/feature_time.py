from datetime import datetime
from typing import Any

from typing_extensions import Annotated

from chalk.features.feature_field import Feature
from chalk.features.feature_wrapper import unwrap_feature

FeatureTime = Annotated[datetime, "__chalk_ts__"]


def feature_time() -> Any:
    return Feature(typ=datetime, is_feature_time=True)


def is_feature_time(f: Any) -> bool:
    """
    Determine whether a feature is a feature time
    :param f: A feature (ie. User.ts)
    :return: True if the feature is a feature time and False otherwise
    """
    return unwrap_feature(f).is_feature_time
