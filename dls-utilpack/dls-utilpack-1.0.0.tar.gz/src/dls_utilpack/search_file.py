import logging
from pathlib import Path

logger = logging.getLogger(__name__)


class SearchFileNotFound(Exception):
    pass


# ----------------------------------------------------------------------------------------
def search_file(search_paths, filename):
    """
    TODO: Better testing in search_file, and handling absolute and cwd-relative files.
    """

    # Strip leading slashes.
    filename = filename.lstrip("/")

    # Check all the paths.
    searched_paths = []
    for search_path in search_paths:
        # Handle case where list item is a dict with path keyword.
        if isinstance(search_path, dict) and "path" in search_path:
            search_path = search_path["path"]

        absolute = Path(search_path) / filename
        if absolute.exists():
            return str(absolute)

        searched_paths.append(search_path)

        # logger.info(f"{absolute} not found")

    raise SearchFileNotFound(f"{filename} not found in search paths {searched_paths}")
