from typing import Any, List, Optional

from chalk.features.dataframe import DataFrame
from chalk.features.feature_field import Feature, feature, has_many, has_one
from chalk.features.feature_set import Features, FeatureSetBase, is_features_cls
from chalk.features.feature_set_decorator import features
from chalk.features.feature_time import FeatureTime, feature_time, is_feature_time
from chalk.features.feature_wrapper import FeatureWrapper, ensure_feature, unwrap_feature
from chalk.features.filter import Filter, TimeDelta, after, before
from chalk.features.hooks import after_all, before_all
from chalk.features.primary import Primary, is_primary
from chalk.features.resolver import Cron, Resolver, ScheduleOptions, offline, online, sink
from chalk.features.tag import Environments, Tags
from chalk.utils import MachineType

__all__ = [
    "Cron",
    "DataFrame",
    "Environments",
    "Feature",
    "FeatureSetBase",
    "FeatureTime",
    "FeatureWrapper",
    "Features",
    "Filter",
    "MachineType",
    "Primary",
    "ScheduleOptions",
    "Tags",
    "TimeDelta",
    "after",
    "after_all",
    "before",
    "before_all",
    "description",
    "ensure_feature",
    "feature",
    "feature_time",
    "features",
    "has_many",
    "has_one",
    "is_feature_time",
    "is_primary",
    "offline",
    "online",
    "owner",
    "sink",
    "tags",
    "unwrap_feature",
]


def owner(f: Any) -> Optional[str]:
    """
    Get the owner for a feature or feature class
    :param f: A feature (ie. User.email or User)
    :return: The owner for a feature or feature class, if it exists.
    Note that the owner could be inherited from the feature class.
    """
    if is_features_cls(f):
        return f.__chalk_owner__
    if isinstance(f, (Feature, FeatureWrapper)):
        feature = unwrap_feature(f)
        return feature.owner
    if isinstance(f, Resolver):
        return f.owner

    raise TypeError(f"Could not determine the owner of {f} as it is neither a Feature or Feature Set")


def description(f: Any) -> Optional[str]:
    """
    Get the description of a feature or feature class
    :param f: A feature or feature class (ie. User.email or User)
    :return: The description given for the feature or feature class.
    """
    if is_features_cls(f):
        return f.__doc__
    if isinstance(f, (Feature, FeatureWrapper)):
        feature = unwrap_feature(f)
        return feature.description
    raise TypeError(f"Could not determine the description of {f} as it is neither a Feature or Feature Set")


def tags(f: Any) -> Optional[List[str]]:
    """
    Get the tags for a feature or feature class
    :param f: A feature or feature class (ie. User.email or User)
    :return: The tags given for the feature or feature class
    Note that the owner can be inherited from the feature class.
    """
    if is_features_cls(f):
        return f.__chalk_tags__
    if isinstance(f, (Feature, FeatureWrapper)):
        feature = unwrap_feature(f)
        return feature.tags
    raise TypeError(f"Could not determine the tags of {f} as it is neither a Feature or Feature Set")
