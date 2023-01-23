from typing import ClassVar, Type, TypeVar

from pydantic import BaseModel


class BaseProjectKitClass:
    project_kit_include_required: ClassVar[bool] = True
    project_kit_include_optional: ClassVar[bool] = True

    @classmethod
    @property
    def project_kit_fields_to_exclude_from_settings_schema(cls) -> set[str]:
        """
        Some required fields for a class are sometimes highly specific to its respective object. These fields should
        be recorded in this class-property to be excluded by the settings generator function
        :return:
        """
        return set()


PYDANTIC_INHERITANCE_ORDER = BaseProjectKitClass, BaseModel

ProjectKitClassCLS = Type[BaseProjectKitClass]
ProjectKitClass = TypeVar("ProjectKitClass", bound=BaseProjectKitClass)


class BaseProjectKitModel(*PYDANTIC_INHERITANCE_ORDER):
    pass
