"""Script to check for available updates."""
import json
from ._utils import _check_required_modules, _INSTALLED_MODULES


try:
    import requests

    _INSTALLED_MODULES["requests"] = True
except ModuleNotFoundError:
    pass

try:
    from packaging.version import Version

    _INSTALLED_MODULES["packaging"] = True
except ModuleNotFoundError:
    pass


@_check_required_modules("requests")
@_check_required_modules("packaging")
def check_update(project_name: str, current_version: str) -> bool:
    """Check version against pypi.org information

    **Requires Requests**
    **Requires Packaging**

    :param project_name: Name of project to check
    :param current_version: Current version of project. Usually from __version__
    :return: Latest version is newer. Returns false if project can't be found
    :rtype: bool
    """

    try:
        latest = Version(
            requests.get(f"https://pypi.org/pypi/{project_name}/json", timeout=10).json()["info"][
                "version"
            ],
        )
    except json.decoder.JSONDecodeError:
        return False
    current_version = Version(current_version)
    return latest > current_version
