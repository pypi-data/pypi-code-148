from datetime import datetime
from pathlib import Path


def get_default_year():
    now = datetime.today()
    return now.year if now.month == 12 else now.year-1


def guess_language(plugins, path: Path=None) -> str:
    languages = [p.__language__ for p in plugins if hasattr(p, '__language__')]

    if not path:
        path = Path()
    cwd = Path(path).resolve()
    for x in reversed(cwd.parents):
        if x.name in languages:
            return x.name
    raise ValueError(f"Unable to guess language from path: {cwd.absolute()}")