from copy import deepcopy
from enum import Enum
from pathlib import Path
from typing import List, Mapping, Tuple, Union
import re
import yaml

from sourcelib.file import File, FileMode


class NoSourceFilesInFolderError(Exception):
    ...


class NonExistentModeInYamlSource(Exception):
    ...


def get_files_from_paths(
    file_cls: Union[str, type],
    mode: Enum,
    paths: List[str],
    filters: List[str],
    excludes: List[str],
    regex=None,
    **kwargs,
):
    files = []
    paths = set(paths)
    for path in paths:
        path = str(Path(path).expanduser())
        if any((exclude in path for exclude in excludes)):
            continue
        if filters and not any((filter in path for filter in filters)):
            continue
        if regex is not None and not re.search(regex, path):
            continue

        files.append(file_cls(mode=mode, path=path, **kwargs))
    return sorted(files, key=lambda k: k.path)


def get_files_from_path(
    file_cls: type, path: str, mode: Enum = FileMode.default, **kwargs
):
    return get_files_from_paths(file_cls, mode, [path], [], [], None, **kwargs)


def get_files_from_folder(
    file_cls: File,
    folder: Union[str, Path],
    mode: Enum = FileMode.default,
    filters: List[str] = (),
    excludes: List[str] = (),
    regex=None,
    recursive=False,
    **kwargs,
):

    all_sources = []
    folder = Path(folder)
    for extension in file_cls.EXTENSIONS:
        paths = (
            folder.rglob("*" + extension) if recursive else folder.glob("*" + extension)
        )
        sources = get_files_from_paths(
            file_cls, mode, paths, filters, excludes, regex, **kwargs
        )
        all_sources.extend(sources)

    if len(all_sources) == 0:
        raise NoSourceFilesInFolderError(file_cls, filters, excludes, regex, folder)
    return all_sources


# YAML_SOURCE_SCHEMA = {"mode": {'File_key': {'path': 'path_to_File', '**kwargs': '**kwargs'}}}


def get_files_from_yaml(
    yaml_source: Union[str, dict],
    file_cls: File,
    mode: Enum = FileMode.default,
    filters=(),
    excludes=(),
    regex=None,
    **kwargs,
):

    data = {}
    if isinstance(yaml_source, Mapping):
        data = deepcopy(yaml_source)
    elif isinstance(yaml_source, (str, Path)):
        with open(yaml_source, encoding="utf-8") as file:
            data = yaml.safe_load(file)

    paths = []
    if mode.name not in data:
        raise NonExistentModeInYamlSource(
            f"mode '{mode.name}' not in data {data.keys()} in: {yaml_source}"
        )

    file_identifier = file_cls.IDENTIFIER
    for item in data[mode.name]:
        if file_identifier in item:
            paths.append(item[file_identifier].pop("path"))
            kwargs.update(item[file_identifier])

    return get_files_from_paths(file_cls, mode, paths, filters, excludes, regex, **kwargs)


def copy_from_yml(
    yaml_source: Union[Path, dict],
    file_cls: File,
    copy_path: Path,
    modes: Tuple[Enum] = (FileMode.default,),
    **kwargs,
):
    data = []
    for mode in modes:
        data.extend(
            get_files_from_yaml(
                yaml_source=yaml_source,
                file_cls=file_cls,
                mode=mode,
                **kwargs,
            )
        )
    for d in data:
        d.copy(copy_path)
