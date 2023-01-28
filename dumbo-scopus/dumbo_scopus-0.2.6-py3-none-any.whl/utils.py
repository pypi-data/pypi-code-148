from pathlib import Path


def is_file_open_by_other_processes(path: Path) -> bool:
    try:
        with open(path, "a"):
            ...
    except PermissionError:
        return True
    else:
        return False
