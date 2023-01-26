
import json
import logging
import subprocess
from pathlib import Path
from typing import Any, Dict, List, Set

from multiversx_sdk_rust_contract_builder.constants import (
    CONTRACT_CONFIG_FILENAME, OLD_CONTRACT_CONFIG_FILENAME)
from multiversx_sdk_rust_contract_builder.errors import ErrKnown
from multiversx_sdk_rust_contract_builder.filesystem import get_all_files


def get_source_code_files_necessary_for_contract(contract_folder: Path, contract_name: str) -> List[Path]:
    source_files: List[Path] = []

    source_files.extend(get_all_source_code_files(contract_folder))
    local_dependencies = get_local_dependencies(contract_folder, contract_name)

    logging.info(f"Found {len(local_dependencies)} local dependencies.")

    for dependency in local_dependencies:
        logging.debug(f"Local dependency: {dependency}")
        source_files.extend(get_all_files(dependency, is_source_code_file))

    return sorted(set(source_files))


def get_all_source_code_files(folder: Path) -> List[Path]:
    return sorted(get_all_files(folder, is_source_code_file))


def is_source_code_file(path: Path) -> bool:
    if path.suffix == ".rs":
        return True
    if path.parent.name == "meta" and path.name == "Cargo.lock":
        return False
    if path.name in ["Cargo.toml", "Cargo.lock", CONTRACT_CONFIG_FILENAME, OLD_CONTRACT_CONFIG_FILENAME]:
        return True
    return False


def replace_all_test_content_with_noop(folder: Path):
    # At this moment (January 2023) we cannot completely exclude test files from the compilation
    # (if we do so, the build throws some errors, in some cases).
    # So we replace all test content with a noop function.
    # This is not ideal, but it works for now.

    logging.info(f"replace_all_test_content_with_noop({folder})")
    test_files = get_all_files(folder, is_test_file)
    for file in test_files:
        file.write_text("fn nothing() {}")


def is_test_file(path: Path) -> bool:
    is_in_tests_folder = any(part in ["test", "tests"] for part in path.parts)
    return path.suffix == ".rs" and is_in_tests_folder


def get_local_dependencies(contract_folder: Path, contract_name: str) -> List[Path]:
    args = ["cargo", "metadata", "--format-version=1"]
    logging.info(f"get_local_dependencies(), running: {args}, with cwd = {contract_folder}")
    metadata_json = subprocess.check_output(args, cwd=contract_folder, shell=False, universal_newlines=True)
    metadata = json.loads(metadata_json)

    logging.info(f"get_local_dependencies(), explore metadata recursively for contract {contract_name}")
    paths = _get_local_dependencies_recursively(metadata, contract_name, set(), 0)
    return list(paths)


def _get_local_dependencies_recursively(cargo_metadata: Dict[str, Any], package_name: str, visited: Set[str], indentation: int) -> Set[Path]:
    if package_name in visited:
        return set()

    visited.add(package_name)

    packages = cargo_metadata.get("packages", [])
    package = next((package for package in packages if package["name"] == package_name), None)
    if not package:
        raise ErrKnown(f"Could not find package {package_name} in project metadata.")

    dependencies = package.get("dependencies", [])
    local_dependencies = [dependency for dependency in dependencies if _is_local_dependency(dependency)]
    paths = set([Path(dependency["path"]) for dependency in local_dependencies])

    logging.debug(f"{indentation * 4 * ' '} ({package_name}): {[dependency['name'] for dependency in local_dependencies]}")

    for dependency in local_dependencies:
        paths |= _get_local_dependencies_recursively(cargo_metadata, dependency["name"], visited, indentation + 1)

    return paths


def _is_local_dependency(dependency: Dict[str, Any]) -> bool:
    return "path" in dependency
