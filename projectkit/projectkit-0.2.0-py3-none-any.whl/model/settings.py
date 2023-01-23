import json
import logging
import platform
from functools import reduce, cached_property
from typing import Any, Callable, ClassVar, Hashable, Iterable, Literal, Optional, Union, TypeVar

import pkg_resources
import tomlkit
import yaml
from pydantic import BaseModel, DirectoryPath, FilePath

from projectkit import PACKAGE_NAME
from projectkit.model.project import ProjectKitClassCLS
from projectkit.utils.map import (
    update_dictionary,
    get_definable_settings,
    update_defined_values,
)
from projectkit.utils.pydantic import CPModel
from projectkit.utils.schema import extended_schema, extended_group_schema
from projectkit.utils.typing import FirstLevelSettings, ProjectKitSupportedFormat, ProjectKitSettingsMap

DISALLOWED_KEYS_IN_SETTINGS_MSG = "{} collides with a built-in settings key in projectkit; refactoring is required"

logger = logging.getLogger(__file__)


class ProjectKitSettings(CPModel):
    project_name: str = ...

    init_input_settings_keys_to_prompt: Optional[dict[str, str]]

    # Defined by choices during the initialization of the project instance, editing this portion should be with caution
    immutable_setting_to_default: Optional[FirstLevelSettings]
    # Settings defined by the meta project developer
    manual_setting_to_default: Optional[dict[str, Any]]

    # The fields in these classes will be included as part of the settings, class derived settings (CDS)
    cds_single_classes_to_derive_settings: Optional[set[ProjectKitClassCLS]]
    cds_class_groups_to_derive_settings: Optional[dict[str, set[ProjectKitClassCLS]]]
    cds_include_field_types: bool = True

    setting_file_stem_suffix: str = "_settings"

    settings_format: ProjectKitSupportedFormat = "toml"

    # To avoid collisions with projectkit native settings fields
    _disallowed_keys_in_root_setting_dict: set[Hashable] = set("immutable")

    @classmethod
    @property
    def settings_file_stem(cls) -> str:
        return f"{cls.project_name}{cls.setting_file_stem_suffix}"

    @classmethod
    @property
    def settings_file_name(cls) -> str:
        return f"{cls.settings_file_stem}.{cls.settings_format}"

    def settings_file_path(self, project_directory: DirectoryPath) -> FilePath:
        """

        :param project_directory: The path to the project directory related to the settings
        :return:
        """
        return project_directory / self.settings_file_name

    def dump_settings(self, settings: ProjectKitSettingsMap, project_directory: DirectoryPath, lock: bool = True) -> None:
        """

        :param settings:
        :param project_directory:
        :param lock: Save a copy of settings since last runtime in a .lock.<FORMAT> file
        """
        match self.settings_format:
            case "toml":
                dumper = tomlkit.dump
            case "yaml":
                dumper = yaml.dump
            case _:
                raise RuntimeError()
        if lock:
            with open(self.settings_lock_file_path(project_directory), "w") as out_settings_lock:
                dumper(self.lock_settings(settings), out_settings_lock)
        with open(self.settings_file_path(project_directory), "w") as out_settings:
            dumper(settings, out_settings)

    def load_settings(self, project_directory: DirectoryPath, check_locked: bool = True) -> ProjectKitSettingsMap:
        match self.settings_format:
            case "toml":
                loader = tomlkit.load
            case "yaml":
                loader = yaml.load
            case _:
                raise RuntimeError()
        with open(self.settings_file_path(project_directory), "r") as in_settings:
            settings = loader(in_settings)

        if check_locked:
            try:
                with open(self.settings_lock_file_path(project_directory), "r") as in_locked_settings:
                    assert loader(in_locked_settings)["Locked"] == settings
            except FileNotFoundError:
                logger.debug(f"Lock file, {self.settings_lock_file_name}, not found in {project_directory}")

        return settings

    def new(self, silent: bool = True) -> ProjectKitSettingsMap:
        result = {}

        if self.immutable_setting_to_default:
            result["immutable"] = self.immutable_setting_to_default

        if self.manual_setting_to_default:
            self._settings_field_not_in_disallowed_keys(self.manual_setting_to_default.keys())
            result.update(self.manual_setting_to_default)

        result.update(self.cds_single_class_derived_settings)
        result.update(self.cds_class_group_derived_settings)

        if not silent:
            print(json.dumps(result, indent=2))

        return result

    def dump_new(self, project_directory: DirectoryPath) -> None:
        self.dump_settings(self.new(silent=True), project_directory)

    def load_old(self, project_directory: DirectoryPath) -> ProjectKitSettingsMap:
        return self.load_settings(project_directory)

    def update(
        self,
        project_directory: DirectoryPath,
        delete_outdated: bool = False,
        dry_run: bool = False,
        silent: bool = False,
    ) -> None:
        old_settings = self.load_old(project_directory)
        new_settings = self.new(silent=True)

        kwargs = {"delete_outdated": delete_outdated}

        for key in ("ingress", "definition_strategies", "perimeter"):
            if key in old_settings:
                try:
                    new_settings[key] = update_dictionary(old_settings[key], new_settings[key], **kwargs)
                except KeyError:
                    pass

        for key in ("manual_reader_kwargs", "experiment"):
            if key in old_settings:
                try:
                    new_settings[key] = update_defined_values(old_settings[key], new_settings[key], **kwargs)
                except KeyError:
                    pass

        if "trial" in old_settings:
            new_settings["trial"]["common"] = update_defined_values(
                old_settings["trial"]["common"], new_settings["trial"]["common"], **kwargs
            )
            common_settings_between_trials = get_definable_settings(new_settings["trial"]["common"])
            for trial_class_name, trial_class_settings in new_settings["trial"]["specific"].items():
                try:
                    new_settings["trial"]["specific"][trial_class_name] = update_defined_values(
                        old_settings["trial"]["specific"][trial_class_name],
                        trial_class_settings,
                        common_settings=common_settings_between_trials,
                        **kwargs,
                    )
                except KeyError:
                    pass

        for field, value in old_settings.items():
            if isinstance(value, dict):
                continue
            if field in new_settings and value:
                new_settings[field] = value

        if not silent:
            print(json.dumps(new_settings, indent=2))

        if not dry_run:
            self.dump_settings(new_settings, project_directory)

    @classmethod
    @property
    def settings_lock_file_name(cls) -> str:
        return f"{cls.settings_file_stem}.lock.{cls.settings_format}"

    def settings_lock_file_path(self, project_directory: DirectoryPath) -> FilePath:
        """

        :param project_directory: The path to the project directory related to the settings
        :return:
        """
        return project_directory / self.settings_lock_file_name

    @classmethod
    def lock_settings(cls, settings: ProjectKitSettingsMap) -> ProjectKitSettingsMap:
        return {
            "Python_version": platform.python_version(),
            "ProjectKit": {
                "format": cls.settings_format,
                "version": pkg_resources.get_distribution(PACKAGE_NAME).version,
            },
            "Locked": settings
        }

    @cached_property
    def cds_single_class_derived_settings(self) -> FirstLevelSettings:
        result = {}
        if self.cds_single_classes_to_derive_settings:
            self._settings_field_not_in_disallowed_keys(
                (cls.__name__ for cls in self.cds_single_classes_to_derive_settings)
            )
            for cls in self.cds_single_classes_to_derive_settings:
                result.update(
                    extended_schema(
                        cls,
                        with_required=cls.project_kit_include_required,
                        with_optional=cls.project_kit_include_optional,
                    )
                )
        return result

    @cached_property
    def cds_class_group_derived_settings(self) -> ProjectKitSettingsMap:
        result = {}
        if self.cds_class_groups_to_derive_settings:
            for group_name, group in self.cds_class_groups_to_derive_settings.items():
                assert (
                        group_name not in self._disallowed_keys_in_root_setting_dict
                ), DISALLOWED_KEYS_IN_SETTINGS_MSG.format(group_name)
                result[group_name] = extended_group_schema(group)
        return result

    @cached_property
    def setting_key_to_project_kit_type(self) -> dict[str, str]:
        result = {}
        if self.immutable_setting_to_default:
            for key in self.immutable_setting_to_default:
                result[key] = "immutable"
        if self.manual_setting_to_default:
            for key in self.manual_setting_to_default:
                result[key] = "manual"
        if self.cds_single_class_derived_settings:
            for key in self.cds_single_class_derived_settings:
                result[key] = "manual"
        return result

    def _settings_field_not_in_disallowed_keys(self, fields: Iterable[Hashable]) -> None:
        for field in fields:
            assert field not in self._disallowed_keys_in_root_setting_dict, DISALLOWED_KEYS_IN_SETTINGS_MSG.format(
                field
            )
