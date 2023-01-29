import json
from operator import itemgetter
from pathlib import Path
from typing import List, Any

import yaml

from .util import ENCODING, TEST, FIX, ORDER, MODE, INIT


def read_configuration(directory: Path) -> List[Any]:
    """
    Extracts every JSON or YAML configuration item from the files in the given directory.

    :param directory: Path to the configuration directory
    :return: aggregated list of configuration items
    """

    print("reading configuration")
    items = []

    for path in directory.iterdir():
        try:
            text = path.read_text(encoding=ENCODING)
        except (OSError, ValueError) as error:
            print(f"'{path.relative_to(directory)}' ignored: {error}")
            continue

        data = yaml.load(text, Loader=yaml.BaseLoader)
        if not isinstance(data, list):
            print(f"'{path.relative_to(directory)}' ignored: not a proper yaml or json list")
        else:
            items.extend(data)

    return items


def validate_tests(items: List[Any]) -> List[dict]:
    """
    Validates the given configuration items into tests.

    :param items: list of configuration items
    :return: a sorted list of tests
    """

    print("validating tests")
    tests = []

    for item in items:
        if not isinstance(item, dict):
            print("ignored, not a dictionary:", json.dumps(item))
            continue

        keys = item.keys()

        if keys not in [{TEST, FIX, ORDER}, {TEST, FIX, ORDER, MODE}]:
            print(f"ignored, keys must match ({TEST}, {FIX}, {ORDER}) or ({TEST}, {FIX}, {ORDER}, {MODE}):", json.dumps(item))
            continue

        if MODE in keys and isinstance(item[MODE], str):  # a single mode as a string is tolerated, but converted into a list for technical purposes
            item[MODE] = [item[MODE]]

        if MODE in keys and (not isinstance(item[MODE], list) or any(not isinstance(value, str) for value in item[MODE])):
            print(f'ignored, value for "{MODE}" can only be a string or a list of strings:', json.dumps(item))
            continue

        if any(not isinstance(item[key], str) for key in [TEST, FIX]):
            print(f'ignored, values for "{TEST}" and "{FIX}" can only be strings:', json.dumps(item))
            continue

        try:
            item[ORDER] = int(item[ORDER])
        except (ValueError, TypeError):
            print(f'ignored, value for "{ORDER}" can only be an integer:', json.dumps(item))
            continue

        tests.append(item)

    return sorted(tests, key=itemgetter(ORDER))


def get_active_mode(mode_file: Path) -> str:
    f"""
    Reads the active mode from the given file, or returns a default "{INIT}" mode.

    :param mode_file: Path to the mode file
    :return: the mode read from the file or "{INIT}"
    """

    try:
        return mode_file.read_text(encoding=ENCODING).strip()
    except (OSError, ValueError):
        return INIT


def filter_active_tests(active_mode: str, tests: List[dict]) -> List[dict]:
    """
    :param active_mode: name of the active mode
    :param tests: list of available tests
    :return: the list of active tests, i.e. tests without any mode or whose modes include the active one
    """

    print("filtering active tests")
    active_tests = []

    for test in tests:
        if not test.get(MODE) or active_mode in test.get(MODE):
            print("active:", json.dumps(test))
            active_tests.append(test)

    return active_tests


class Watcher:
    """
    Will watch over the given configuration paths and monitor possible changes:

    * tests directory timestamp
    * available tests
    * active mode
    * active tests

    :param tests_directory: Path to the tests directory
    :param mode_file: Path to the mode file
    """

    def __init__(self, tests_directory: Path, mode_file: Path):
        self.tests_directory = tests_directory
        self.mode_file = mode_file

        self.mtime = 0
        self.tests = []
        self.active_mode = INIT
        self.active_tests = []

    def tests_directory_has_changed(self) -> bool:
        """
        :return: whether the tests directory has changed since the last call
        """

        # monitoring the directory modification timestamp doesn't cover every possible file change but it's very cheap
        new_mtime = self.tests_directory.stat().st_mtime
        if new_mtime == self.mtime:
            return False
        print("tests directory has changed")
        self.mtime = new_mtime
        return True

    def tests_have_changed(self) -> bool:
        """
        :return: whether the tests have changed since the last call
        """

        new_tests = validate_tests(read_configuration(self.tests_directory))
        if new_tests == self.tests:
            return False
        print("tests have changed")
        self.tests = new_tests
        return True

    def active_mode_has_changed(self) -> bool:
        """
        :return: whether the active mode has changed since the last call
        """

        new_active_mode = get_active_mode(self.mode_file)
        if new_active_mode == self.active_mode:
            return False
        print("active mode has changed:", new_active_mode)
        self.active_mode = new_active_mode
        return True

    def refresh_active_tests_if_necessary(self) -> None:
        """
        Refreshes the active tests only if the tests' directory, the available tests or the active mode have changed.
        It may not be the most performant, but the logs are much clearer.
        """

        if (self.tests_directory_has_changed() and self.tests_have_changed()) | self.active_mode_has_changed():
            self.active_tests = filter_active_tests(self.active_mode, self.tests)
