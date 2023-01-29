from typing import List
import pathlib
import os


def run(root_path: str, search_folders: List[str], file_extensions: List[str], prepend_root: bool):
    files = []

    root_path = pathlib.Path(root_path)
    for folder in search_folders:
        search_path = root_path.joinpath(folder)
        temp_files = _find_files(search_path, file_extensions)

        if not prepend_root:
            temp_files = [str(pathlib.Path(file_path).relative_to(root_path)) for file_path in temp_files]
        files += temp_files

    files = [path.replace("\\", "/") for path in files]
    return files


def _find_files(search_path: pathlib.Path, file_extensions: List[str]):
    files = []
    for extension in file_extensions:
        files += _walk_tree(search_path, extension)

    return files


def _walk_tree(search_path: pathlib.Path, file_extension: str):
    file_list = []
    for root, sub_dirs, files in os.walk(search_path):
        if files:
            file_list += [os.path.join(root, file) for file in files if file.endswith(file_extension)]

    return file_list
