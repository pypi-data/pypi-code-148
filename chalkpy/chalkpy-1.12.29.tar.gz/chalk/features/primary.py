from typing import Any, Type, TypeVar, cast

from typing_extensions import Annotated

from chalk.features.feature_wrapper import unwrap_feature

T = TypeVar("T")


class PrimaryMeta(type):
    def __getitem__(self, item: Type[T]) -> Type[T]:
        return cast(Type[T], Annotated[item, "__chalk_primary__"])


Primary = PrimaryMeta("Primary", (object,), {})


def is_primary(f: Any) -> bool:
    """
    Determine whether a feature is a primary key
    :param f: A feature (ie. User.email)
    :return: True if the feature is primary and False otherwise
    """
    return unwrap_feature(f).primary
